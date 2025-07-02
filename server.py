import socket


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # This will create a TCP/IPv4 socket
server_socket.bind(('localhost', 6666))  # Bind the socket to an address and port
server_socket.listen(5)  # Listen for incoming connections


# Now we have to wait for a connection
client_connection, client_address = server_socket.accept()  # Accept a connection



# After accepting a connection, we can receive data from the client
request_data = client_connection.recv(1024)  # Receive data from the client
print(f"Received request: {request_data.decode()}")  # Print the received data
request_data = request_data.decode()


#Now we can parse the request data to get the method, path, and headers
def parse_request(request_data):
    lines = request_data.split('\r\n')

    method, path, version = lines[0].split(' ')

    # Parse headers
    headers = {}
    for line in lines[1:]:
        if ':' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
        


    # Parse body if present
    body = ''
    if '\r\n\r\n' in request_data:
        body = request_data.split('\r\n\r\n')[1]
    
    return {
        'method': method,
        'version': version,
        'path': path,
        'headers': headers,
        'body': body
    }



parsed_request = parse_request(request_data)
print(f"Parsed request: {parsed_request}")  # Print the parsed request


# Time to parse the request handling and routing
'''
    This is where we will handle the request and route it to the appropriate handler.
    For now, we will just print the method and path.
    Nah we will create a application and a routes from where the request will redirect and get the response.
'''

# So this is after the request come to the load balancer and then we have to proceed further.

def handle_request(parsed_request):
    method = parsed_request['method']
    path = parsed_request['path']
    
    # For now, we will just print the method and path
    print(f"Handling request: {method} {path}")
    
    # Here we can add logic to handle different methods and paths
    if method == 'GET':
        if path == '/':
            response_body = '<h1>Welcome to the Pico HTTP Server!</h1>'
            status_code = '200 OK'
        else:
            response_body = '<h1>404 Not Found</h1>'
            status_code = '404 Not Found'
    else:
        response_body = '<h1>405 Method Not Allowed</h1>'
        status_code = '405 Method Not Allowed'
    
    return status_code, response_body