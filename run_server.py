import uvicorn
import os
from pathlib import Path

if __name__ == "__main__":
    # Ensure data directories exist
    Path("data").mkdir(exist_ok=True)
    Path("data/csv").mkdir(exist_ok=True)
    Path("data/mdf").mkdir(exist_ok=True)
    Path("uploads").mkdir(exist_ok=True)
    
    # Get configuration from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    print(f"Starting Automotive Analysis API on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"API docs will be available at: http://{host}:{port}/docs")
    print(f"Data directory: {os.path.abspath('data')}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )