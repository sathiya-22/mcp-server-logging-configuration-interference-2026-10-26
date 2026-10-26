import logging
import time

# This is a mock MCP server that simulates the logging behavior of a real one.
# It sets up its own logging, which *would* interfere if not for the fixer.

class MockMCPServer:
    """
    A mock MCP server that simulates its own logging setup and activity.
    """
    def __init__(self):
        self._logger = logging.getLogger("mcp.server")
        self._is_running = False

    def start(self):
        """
        Simulates the MCP server's initialization, including its own logging setup.
        In a real MCP server, this might involve reconfiguring the root logger
        or adding handlers that conflict with the application.
        """
        if not self._is_running:
            # Simulate MCP server configuring its own logging
            # This is the problematic part that the fixer addresses.
            # We'll set a specific handler and formatter for the mock MCP logger.
            mcp_handler = logging.StreamHandler()
            mcp_formatter = logging.Formatter('[MCP] %(asctime)s - %(levelname)s - %(name)s - %(message)s')
            mcp_handler.setFormatter(mcp_formatter)

            # Ensure this logger doesn't propagate to root, if MCP sets its own root handlers
            # In a real scenario, MCP might modify the root directly.
            self._logger.propagate = False
            self._logger.addHandler(mcp_handler)
            self._logger.setLevel(logging.DEBUG)

            self._is_running = True
            self._logger.info("Mock MCP Server starting...")
        else:
            self._logger.warning("Mock MCP Server is already running.")

    def process_something(self):
        """Simulates the MCP server doing some work and logging."""
        if self._is_running:
            self._logger.debug("Processing client request...")
            time.sleep(0.1) # Simulate work
            self._logger.info("Request processed successfully.")
        else:
            self._logger.error("Cannot process; Mock MCP Server is not started.")

    def stop(self):
        """Simulates stopping the MCP server."""
        if self._is_running:
            self._logger.info("Mock MCP Server stopping.")
            # Clean up its specific handlers
            for handler in self._logger.handlers[:]:
                self._logger.removeHandler(handler)
            self._is_running = False
        else:
            self._logger.warning("Mock MCP Server is not running.")
