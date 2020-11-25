from socket import *

s = socket()
s.bind(("0.0.0.0",8888))
s.listen(5)

c,addr = s.accept()

print("Connect from",addr)

data = c.recv(1024 * 10)
print(data.decode())

response = """HTTP/1.1 200 OK
Content-Type:text/html

<h1>Hello world</h1>
"""

c.send(response.encode())


c.close()
s.close()