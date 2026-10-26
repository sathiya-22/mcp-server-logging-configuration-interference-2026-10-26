import logging
import time
from mcp_log_fixer import run_mcp_with_preserved_logging, preserve_logging
from mcp_server_mock import MockMCPServer

# --- DEMO 1: Using run_mcp_with_preserved_logging context manager ---
print("--- DEMO 1: Context Manager ---")

# Configure application's logging FIRST
logging.basicConfig(level=logging.INFO,
                    format='[APP_DEMO1] %(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

app_logger_1 = logging.getLogger("app.demo1")
app_logger_1.info("Application logging configured for Demo 1.")

# Now, initialize the MCP server using the context manager
with run_mcp_with_preserved_logging():
    app_logger_1.info("Inside MCP context (Demo 1). MCP server is initializing...")
    mcp_server_1 = MockMCPServer() # Your actual MCP server initialization here
    mcp_server_1.start()
    app_logger_1.info("MCP server started. Application logs should still be visible.")
    mcp_server_1.process_something() # Simulate MCP server activity
    time.sleep(0.2)
    mcp_server_1.stop()
    app_logger_1.info("MCP server stopped.")

app_logger_1.info("Outside MCP context (Demo 1). Application logging still working as expected.")
print("\n" + "="*80 + "\n")


# --- DEMO 2: Using preserve_logging decorator ---
print("--- DEMO 2: Decorator ---")

# Configure application's logging FIRST
logging.basicConfig(level=logging.DEBUG, # Different level for demo
                    format='[APP_DEMO2] %(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    handlers=[logging.StreamHandler()])

app_logger_2 = logging.getLogger("app.demo2")
app_logger_2.info("Application logging configured for Demo 2.")

@preserve_logging
def run_my_mcp_workflow_decorated():
    app_logger_2.info("Inside decorated function (Demo 2). MCP server initializing...")
    mcp_server_2 = MockMCPServer()
    mcp_server_2.start()
    app_logger_2.info("MCP server started via decorator. App logs OK.")
    mcp_server_2.process_something()
    time.sleep(0.2)
    mcp_server_2.stop()
    app_logger_2.info("MCP server stopped via decorator.")

app_logger_2.info("Application logging configured before calling decorated function.")
run_my_mcp_workflow_decorated()
app_logger_2.info("Application logging still working after decorated function call.")
print("\n" + "="*80 + "\n")

print("Demo finished. Observe that application logs were never clobbered.")
