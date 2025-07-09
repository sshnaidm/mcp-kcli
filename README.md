# mcp-kcli

A [FastMCP](https://github.com/sshaidm/fastmcp) server that acts as a wrapper around the `kcli` tool to manage virtual machines.

## Description

This server exposes `kcli` functionalities through a simple API, allowing remote execution of `kcli` commands. The primary tool available is `list_vms`, which retrieves a list of virtual machines from a specified host.

## Prerequisites

- Python 3.8+
- kcli installed and configured.
- Pip for installing Python packages.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/mcp-kcli.git
    cd mcp-kcli
    ```

2.  **Create a `requirements.txt` file** with the following content:
    ```
    fastmcp
    pydantic
    uvicorn[standard]
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure `kcli` path (if needed):**
    The server expects the `kcli` binary to be in your system's `PATH`. If it's located elsewhere, you can specify its path using the `KCLI_BIN` environment variable:
    ```bash
    export KCLI_BIN=/path/to/your/kcli
    ```

## Usage

### Running the Server

You can run the server using `fastmcp`:

```bash
fastmcp run --port 5005 mcp.py
```

You should see output indicating the server is running, typically on `http://127.0.0.1:5005`.

### Interacting with the API

The server exposes a tool named `list_vms`. You can interact with it by sending a POST request to the `/mcp` endpoint.

**Endpoint:** `POST /mcp`

**Request Body:**

The request body should be a JSON object specifying the tool to run and its parameters.

```json
{
  "tool": "list_vms",
  "params": {
    "host": "your-hypervisor-host"
  }
}
```

-   `tool`: The name of the tool to execute (`list_vms`).
-   `params.host`: The hostname or IP address of the hypervisor where `kcli` will list the VMs.

#### Example using `curl`

```bash
curl -X POST http://127.0.0.1:5005/mcp \
-H "Content-Type: application/json" \
-d '{
  "tool": "list_vms",
  "params": {
    "host": "kvm-host.example.com"
  }
}'
```

A successful request will return a JSON array with VM details. If an error occurs (e.g., the host is unreachable), it will return a JSON object with an error message.
