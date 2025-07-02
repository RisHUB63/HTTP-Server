# HTTP Request Flow: From Client to Server and Back

This document explains the complete journey of an HTTP request through various system components.

## Architecture Overview
[Client] → DNS → TCP Handshake → HTTP Request → Load Balancer → Web Server → App Server →
Database → App Server → Web Server → Load Balancer → HTTP Response → [Client]


## HTTP Server Components

### Network Layer
- **Port Listening**:
  - HTTP: 80
  - HTTPS: 443
- **Protocol Handling**:
  - Manages TCP/IP connections
  - Handles socket management

### Request Parser
Extracts:
- HTTP Method: [POST, PUT, GET, DELETE, OPTIONS, PATCH]
- URI
- Headers
- Body
- Query Parameters

### Routing Mechanism
- Static URL routing
- RESTful API routing

### Response Generator
- Status codes
- Response Body:
  - Success
  - Failure

### Concurrency Model
- Multi-threading
- Connection pooling

## Sequence Diagram
```mermaid
sequenceDiagram
    participant Client
    participant DNS
    participant LB as Load Balancer
    participant App as Application Server

    Client->>DNS: Query "www.xyz.com"
    DNS-->>Client: Returns LB IP (e.g., 203.0.113.42)
    
    Note right of Client: TCP 3-Way Handshake
    Client->>LB: SYN (Seq=100)
    LB-->>Client: SYN-ACK (Seq=300, Ack=101)
    Client->>LB: ACK (Seq=101, Ack=301)
    
    Note right of Client: HTTP Request
    Client->>LB: GET /user/v1/list HTTP/1.1
    LB->>App: New TCP handshake → Forward request
    App->>LB: HTTP/1.1 200 OK (with data)
    LB->>Client: Forward response
    
    Note right of Client: Connection teardown (if keep-alive=false)
    Client->>LB: FIN
    LB->>App: FIN
    App->>LB: ACK
    LB->>Client: ACK
```

## HTTP Request Flow

```text
1. Client Request
   │
   ▼
2. DNS Resolution
   │  www.xyz.com → 13.224.158.186 (Load Balancer IP)
   │
   ▼
3. TCP 3-Way Handshake
   │  Client              Load Balancer
   │    │───SYN───────▶│
   │    │◀──SYN-ACK───│
   │    │───ACK───────▶│
   │
   ▼
4. Load Balancer Processing
   │  • Health checks
   │  • Routing algorithm
   │  • Backend selection
   │
   ▼
5. Application Processing
   │  • New TCP connection
   │  • Request forwarding
   │  • Business logic
   │  • Database queries
   │
   ▼
6. Response Return
   │  App Server → Load Balancer → Client
   │
   ▼
7. Connection Termination
   │  (If keep-alive=false)
