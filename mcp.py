#!/usr/bin/env python3
# Copyright (c) 2024 Sagi Shnaidman, Red Hat.

import os
import subprocess
from typing import Any

from fastmcp import FastMCP
from pydantic import BaseModel, Field

KCLI_BIN = os.getenv("KCLI_BIN", "kcli")
if not os.path.isfile(KCLI_BIN):
    raise FileNotFoundError(
        f"KCLI binary not found at {KCLI_BIN}. Please set the KCLI_BIN environment variable to the correct path."
    )

# Initialize FastMCP server
mcp = FastMCP(name="kcli", description="KCLI is a tool to work with virtual machines on different hosts.")


class KCLIRequest(BaseModel):
    """
    Schema for KCLI request.
    """

    host: str = Field(
        ...,
        description="The hostname or host IP to execute KCLI commands for virtual machines",
    )


def list_vms(host: str) -> dict[str, Any]:
    """
    Discover all virtual machines running on host
    Example input: {"host": "192.168.105.2"} or {"host": "myhostname"}
    Example output: [
        {
            "name": "virtual_machine_name-installer",
            "nets": [
            {
                "device": "eth0",
                "mac": "aa:aa:bb:bb:cc:cc",
                "net": "baremetal",
                "type": "bridge"
            }
            ],
            "disks": [],
            "id": "c8de4f1b-25f9-4467-a14a-2436fbbf50d8",
            "user": "cloud-user",
            "owner": "userowner",
            "image": "centos-x86_64-kvm.qcow2",
            "plan": "my_plan",
            "profile": "kvirt",
            "creationdate": "02-06-2025 06:01",
            "ip": "192.168.105.39",
            "ips": [
                "192.168.105.39",
                "2000:11:0:111:1111:ff:1111:11"
            ],
            "status": "up"
        }
    ]
    """
    try:
        result = subprocess.run(
            [KCLI_BIN, "-C", host, "list", "vms", "-o", "json"],
            capture_output=True,
            text=True,
            check=True,  # Use check=True to automatically raise CalledProcessError on non-zero exit codes
        )
        return result.stdout

    except subprocess.CalledProcessError as e:
        error_message = f"KCLI command failed with exit code {e.returncode}: {e.stderr.strip()}"
        print(error_message)
        return {"status": "error", "message": error_message}
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        return {"status": "error", "message": error_message}


@mcp.tool(
    name="list_vms",
    description="""
        Retrieves list of virtual machines in JSON format by hostname or IP
        Example input: {'host': '192.168.105.2'} or {'host': 'myhostname'}
        Example output: [{"name": .... }]
        """,
)
async def get_virtual_machines(params: KCLIRequest) -> dict[str, Any]:
    """
    Asynchronously gets list of virtual machines on server with their info
    :param params: KCLIRequest containing the host information
    :return: List of virtual machines with their details or error message
    """
    return list_vms(params.host)


# --- Server Execution ---
if __name__ == "__main__":
    print("Starting FastMCP server for KCLI. Access it at http://127.0.0.1:5005/mcp")
    # To run this server as HTTP, execute:
    # fastmcp run --port 5005 --host 127.0.0.1 -t streamable-http mcp.py
    mcp.run()
