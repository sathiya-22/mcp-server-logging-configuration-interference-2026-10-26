import logging
import contextlib
import functools
import copy

_logger = logging.getLogger(__name__)

@contextlib.contextmanager
def run_mcp_with_preserved_logging():
    """
    A context manager that preserves the application's logging configuration
    before any MCP server initialization that might override it.

    It captures the state of all loggers and handlers before entering the
    context and restores them upon exiting, ensuring MCP's internal logging
    setup doesn't interfere with the main application's logging.
    """
    _logger.debug("Attempting to preserve logging configuration...")

    # Store current logging state
    original_logging_config = {
        name: copy.deepcopy(logger.__dict__)
        for name, logger in logging.root.manager.loggerDict.items()
    }
    original_root_handlers = copy.deepcopy(logging.root.handlers)
    original_root_level = logging.root.level
    original_disable_existing_loggers = logging.root.manager.disable_existing_loggers

    # Clear root handlers temporarily to prevent MCP from attaching to them
    # and potentially duplicate or override formatting.
    # We will restore them later.
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    _logger.debug("Original logging configuration saved. Root handlers temporarily cleared.")

    try:
        yield
    finally:
        _logger.debug("Restoring logging configuration...")

        # First, clear any handlers MCP might have added to the root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Restore original root handlers
        for handler in original_root_handlers:
            logging.root.addHandler(handler)
        logging.root.setLevel(original_root_level)
        logging.root.manager.disable_existing_loggers = original_disable_existing_loggers

        # Restore individual loggers (levels, handlers, etc.)
        for name, original_attrs in original_logging_config.items():
            logger = logging.getLogger(name)
            # Clear existing handlers first
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            
            # Restore attributes. Be careful not to overwrite live objects like `manager`
            # or `parent`, but rather state like `level`, `propagate`, `disabled`, `handlers`.
            for attr, value in original_attrs.items():
                if attr not in ['manager', 'parent', 'name', 'filters', 'handlers']:
                    setattr(logger, attr, value)
            
            # Restore handlers for this specific logger
            if 'handlers' in original_attrs:
                for handler in original_attrs['handlers']:
                    logger.addHandler(handler)
        
        _logger.debug("Logging configuration restored.")


def preserve_logging(func):
    """
    A decorator that applies the `run_mcp_with_preserved_logging` context manager
    to a function.

    Use this if your MCP server initialization and usage is encapsulated within
    a single function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with run_mcp_with_preserved_logging():
            return func(*args, **kwargs)
    return wrapper
