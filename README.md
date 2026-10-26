## MCP Server Logging Configuration Interference Fixer

### The Problem and Who It Affects

The Model Context Protocol (MCP) server, while a crucial component in the agentic AI ecosystem, has a known issue: it aggressively configures its own logging upon initialization. This often overrides or interferes with an application's pre-existing logging setup, leading to lost application logs, unexpected log formats, or a general lack of control over the logging output. Developers building applications that integrate with MCP servers frequently encounter this frustration, as it hinders their ability to debug and monitor their own application's behavior.

### Why this Project Shape/Stack Was Chosen

This prototype is a Python package because:
1.  **MCP Server's Primary Ecosystem:** The MCP server itself is often integrated into Python applications, making a Python-based solution the most natural fit for developers experiencing this issue.
2.  **Standard Python Logging:** Python's `logging` module is powerful and flexible. The problem stems from MCP's interaction with this module, and a Python solution can directly address and mitigate that interference.
3.  **Ease of Integration:** A small Python utility package can be easily incorporated into existing Python projects with minimal overhead, providing a clear and direct solution to the logging conflict.

This project *does not* involve LLMs directly, as the problem is purely an infrastructure/configuration concern regarding the MCP server's internal behavior and its interaction with the Python `logging` module.

### Setup and Usage Instructions (Zero API Keys Required)

This project provides a simple utility function to wrap your MCP server initialization, preventing it from clobbering your application's logging configuration.

1.  **Install:**
    Create a virtual environment and install the package:

        python -m venv venv
        source venv/bin/activate  # On Windows: venv\Scripts\activate
        pip install .

2.  **Integrate into your application:**
    Instead of directly importing and initializing the MCP server, use the `mcp_log_fixer.run_mcp_with_preserved_logging` context manager or decorator.

    **Example using the context manager:**

    ```python
    import logging
    from mcp_log_fixer import run_mcp_with_preserved_logging
    from mcp_server_mock import MockMCPServer # This is a mock for demonstration

    # Configure your application's logging FIRST
    logging.basicConfig(level=logging.INFO,
                        format='[APP] %(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

    app_logger = logging.getLogger(__name__)
    app_logger.info("Application logging configured and active.")

    # Now, initialize the MCP server using the context manager
    with run_mcp_with_preserved_logging():
        app_logger.info("Inside MCP context. MCP server is initializing...")
        mcp_server = MockMCPServer() # Your actual MCP server initialization here
        mcp_server.start()
        app_logger.info("MCP server started. Application logs should still be visible.")
        mcp_server.process_something() # Simulate MCP server activity
        mcp_server.stop()

    app_logger.info("Outside MCP context. Application logging still working as expected.")
    ```

    **Example using the decorator (for functions that initialize and run MCP):**

    ```python
    import logging
    from mcp_log_fixer import preserve_logging
    from mcp_server_mock import MockMCPServer

    logging.basicConfig(level=logging.INFO,
                        format='[DECORATOR_APP] %(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler()])

    app_logger = logging.getLogger(__name__)

    @preserve_logging
    def run_my_mcp_workflow():
        app_logger.info("Inside decorated function. MCP server initializing...")
        mcp_server = MockMCPServer()
        mcp_server.start()
        app_logger.info("MCP server started via decorator. App logs OK.")
        mcp_server.process_something()
        mcp_server.stop()
        app_logger.info("MCP server stopped via decorator.")

    app_logger.info("Application logging configured before decorator.")
    run_my_mcp_workflow()
    app_logger.info("Application logging still working after decorated function.")
    ```

3.  **Run the demo:**
    The `demo.py` file showcases both methods. After installation, simply run:

        python demo.py

    You will observe that the application's logging configuration remains intact, and both application-specific logs and (mock) MCP server logs are displayed according to the application's setup, without interference.

### Optional Real-LLM Adapter

This project does not include an LLM adapter because the problem it solves is purely about logging configuration and infrastructure, not LLM interaction or processing.
