import unittest
from types import SimpleNamespace

from conjur.api.ssl_client import SSLClient

GITHUB_FINGERPRINT = "54:C5:A2:27:06:92:CF:D1:1C:24:A3:92:96:41:49:06:21:B0:45:30"
GITHUB_CERT = \
'''-----BEGIN CERTIFICATE-----
MIIE7jCCBHSgAwIBAgIQBGv4V/rhZO4SCgtfMpPGOTAKBggqhkjOPQQDAzBWMQsw
CQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMTAwLgYDVQQDEydEaWdp
Q2VydCBUTFMgSHlicmlkIEVDQyBTSEEzODQgMjAyMCBDQTEwHhcNMjEwMzEyMDAw
MDAwWhcNMjIwMzIzMjM1OTU5WjBmMQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2Fs
aWZvcm5pYTEWMBQGA1UEBxMNU2FuIEZyYW5jaXNjbzEVMBMGA1UEChMMR2l0SHVi
LCBJbmMuMRMwEQYDVQQDEwpnaXRodWIuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAE2NKiDAGKpIeEu5Zc3atS11fP5PWbOdYtBDm7XKkGoHlyHIxPuuKc0wqo
9o4PK4BzXugwFGiwR/ycuVr/ZTcTUqOCAxIwggMOMB8GA1UdIwQYMBaAFAq8CCkX
jKU5bXoOzjPHLrPt+8N6MB0GA1UdDgQWBBS08xJCml9AyxzY6VeFeTwgBhfaWDAl
BgNVHREEHjAcggpnaXRodWIuY29tgg53d3cuZ2l0aHViLmNvbTAOBgNVHQ8BAf8E
BAMCB4AwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMIGXBgNVHR8EgY8w
gYwwRKBCoECGPmh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydFRMU0h5
YnJpZEVDQ1NIQTM4NDIwMjBDQTEuY3JsMESgQqBAhj5odHRwOi8vY3JsNC5kaWdp
Y2VydC5jb20vRGlnaUNlcnRUTFNIeWJyaWRFQ0NTSEEzODQyMDIwQ0ExLmNybDA+
BgNVHSAENzA1MDMGBmeBDAECAjApMCcGCCsGAQUFBwIBFhtodHRwOi8vd3d3LmRp
Z2ljZXJ0LmNvbS9DUFMwgYMGCCsGAQUFBwEBBHcwdTAkBggrBgEFBQcwAYYYaHR0
cDovL29jc3AuZGlnaWNlcnQuY29tME0GCCsGAQUFBzAChkFodHRwOi8vY2FjZXJ0
cy5kaWdpY2VydC5jb20vRGlnaUNlcnRUTFNIeWJyaWRFQ0NTSEEzODQyMDIwQ0Ex
LmNydDAMBgNVHRMBAf8EAjAAMIIBBgYKKwYBBAHWeQIEAgSB9wSB9ADyAHcAKXm+
8J45OSHwVnOfY6V35b5XfZxgCvj5TV0mXCVdx4QAAAF4J1lR5QAABAMASDBGAiEA
9PC30XzJepYPompNYMDjq9oow8xEAbDAzxZbF0e2HDQCIQC20gF9ohk20paUvsq+
oTXhIwwoyq4TAPprf4Ii5d2M9AB3ACJFRQdZVSRWlj+hL/H3bYbgIyZjrcBLf13G
g1xu4g8CAAABeCdZUjQAAAQDAEgwRgIhANnbglRYcck1OgSk9B6ItU7CpDBJnbdP
SxcIyyAY1If8AiEA0G8HucONc8DcsAQg8+MB7Ms0gTpz5Qs41LLiJ+LLyb4wCgYI
KoZIzj0EAwMDaAAwZQIwflk1MqBiRbkppu+8NqxY3TPzP5XwfZLS75/4aGNigtoY
53Ui/QwQmKtZII7AB7V1AjEAntfvfSN1M9pshLFMV2CCDctp0955sxexDBasHXSN
VRFc5ZyUMUiWhyo8siO3bcxF
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
MIIEQzCCAyugAwIBAgIQCidf5wTW7ssj1c1bSxpOBDANBgkqhkiG9w0BAQwFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBD
QTAeFw0yMDA5MjMwMDAwMDBaFw0zMDA5MjIyMzU5NTlaMFYxCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxMDAuBgNVBAMTJ0RpZ2lDZXJ0IFRMUyBI
eWJyaWQgRUNDIFNIQTM4NCAyMDIwIENBMTB2MBAGByqGSM49AgEGBSuBBAAiA2IA
BMEbxppbmNmkKaDp1AS12+umsmxVwP/tmMZJLwYnUcu/cMEFesOxnYeJuq20ExfJ
qLSDyLiQ0cx0NTY8g3KwtdD3ImnI8YDEe0CPz2iHJlw5ifFNkU3aiYvkA8ND5b8v
c6OCAa4wggGqMB0GA1UdDgQWBBQKvAgpF4ylOW16Ds4zxy6z7fvDejAfBgNVHSME
GDAWgBQD3lA1VtFMu2bwo+IbG8OXsj3RVTAOBgNVHQ8BAf8EBAMCAYYwHQYDVR0l
BBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMBIGA1UdEwEB/wQIMAYBAf8CAQAwdgYI
KwYBBQUHAQEEajBoMCQGCCsGAQUFBzABhhhodHRwOi8vb2NzcC5kaWdpY2VydC5j
b20wQAYIKwYBBQUHMAKGNGh0dHA6Ly9jYWNlcnRzLmRpZ2ljZXJ0LmNvbS9EaWdp
Q2VydEdsb2JhbFJvb3RDQS5jcnQwewYDVR0fBHQwcjA3oDWgM4YxaHR0cDovL2Ny
bDMuZGlnaWNlcnQuY29tL0RpZ2lDZXJ0R2xvYmFsUm9vdENBLmNybDA3oDWgM4Yx
aHR0cDovL2NybDQuZGlnaWNlcnQuY29tL0RpZ2lDZXJ0R2xvYmFsUm9vdENBLmNy
bDAwBgNVHSAEKTAnMAcGBWeBDAEBMAgGBmeBDAECATAIBgZngQwBAgIwCAYGZ4EM
AQIDMA0GCSqGSIb3DQEBDAUAA4IBAQDeOpcbhb17jApY4+PwCwYAeq9EYyp/3YFt
ERim+vc4YLGwOWK9uHsu8AjJkltz32WQt960V6zALxyZZ02LXvIBoa33llPN1d9R
JzcGRvJvPDGJLEoWKRGC5+23QhST4Nlg+j8cZMsywzEXJNmvPlVv/w+AbxsBCMqk
BGPI2lNM8hkmxPad31z6n58SXqJdH/bYF462YvgdgbYKOytobPAyTgr3mYI5sUje
CzqJx1+NLyc8nAK8Ib2HxnC+IrrWzfRLvVNve8KaN9EtBH7TuMwNW4SpDCmGr6fY
1h3tDjHhkTb9PA36zoaJzu0cIw265vZt6hCmYWJC+/j+fgZwcPwL
-----END CERTIFICATE-----
'''

'''
Validates that a socket can be opened with an endpoint 
and a certificate and its fingerprint is returned
'''
class SSLServiceTest(unittest.TestCase):
    ssl_service = SSLClient()

    @unittest.skip('Github certificate fingerpring is not static')
    def test_service_gets_and_returns_fingerprint_and_certificate(self):
        url = {'hostname': 'github.com', 'port': 443}
        url = SimpleNamespace(**url)
        fingerprint, readable_certificate = self.ssl_service.get_certificate(url.hostname, url.port)
        # These certificate will expire in 2022 which means this test will fail.
        # If this is the case, update the expected output
        self.assertEquals(fingerprint, GITHUB_FINGERPRINT)
        self.assertEquals(readable_certificate, GITHUB_CERT)
