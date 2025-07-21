# Data Analysis Using Generative AI - IAV Zio Insight Replacement

## 📋 Task Overview

This project replaces IAV Zio Insight functionality with a REST API powered by Large Language Model (LLM) capabilities. The system automatically generates automotive data analyses from natural language descriptions and signal information.

### 🎯 Task Requirements Met

✅ **REST API Development**: FastAPI-based service that processes automotive measurement data  
✅ **MDF/CSV Data Processing**: Handles provided vehicle measurement files  
✅ **Signal Recognition**: Processes `Eng_nEng10ms`, `Eng_uBatt`, `FuSHp_pRailBnk1`  
✅ **Natural Language Analysis**: Interprets requests like "create a histogram of battery voltage"  
✅ **IAV Zio Insight Compatible**: Generates similar multi-vehicle stacked histograms  
✅ **Automated Analysis**: Replaces manual analysis tool workflow  

## 🚗 Supported Automotive Signals

| Signal | Description | Unit | Example Usage |
|--------|-------------|------|---------------|
| `Eng_nEng10ms` | Engine speed | rpm | "Show engine speed distribution" |
| `Eng_uBatt` | Battery voltage | mV/V | "Create a histogram of battery voltage" |
| `FuSHp_pRailBnk1` | Fuel rail pressure | MPa | "Display fuel pressure across vehicles" |

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Data Structure

Run `analysis.ipynb` to get csv data from mdf files & Ensure your CSV files are in the `data/csv/` directory:
```
data/csv/
├── Vehicle01_meas4.ChannelGroup_0.csv
├── Vehicle01_meas4.ChannelGroup_1.csv
├── ... (all channel groups for all vehicles)
```

### 3. Start the API Server

```bash
python run_server.py
```

Expected output:
```
Starting Automotive Analysis API on localhost:8000
Loaded Vehicle01_meas4.ChannelGroup_0.csv: 25064 rows, 3 columns
Loaded Vehicle01_meas4.ChannelGroup_1.csv: 75191 rows, 5 columns
... (loading all CSV files)
API docs will be available at: http://localhost:8000/docs
```

### 4. Run Task Demonstration

In a new terminal:
```bash
python task_demo.py
```

## 📊 Task Demonstration Results

The `task_demo.py` script tests all task requirements and generates:

### Battery Voltage Analysis (IAV Zio Insight Style)
```json
{
  "signal_descriptions": {
    "Eng_uBatt": "Battery voltage in mV"
  },
  "analysis_description": "Create a histogram of the battery voltage"
}
```
**Output**: `task_battery_voltage.png` - Multi-vehicle stacked histogram

### Fuel Pressure Distribution
```json
{
  "signal_descriptions": {
    "FuSHp_pRailBnk1": "Fuel Pressure"
  },
  "analysis_description": "Show fuel pressure distribution"
}
```
**Output**: `task_fuel_pressure.png` - Pressure distribution analysis

### Engine Speed Analysis
```json
{
  "signal_descriptions": {
    "Eng_nEng10ms": "Engine speed"
  },
  "analysis_description": "Display engine speed histogram"
}
```
**Output**: `task_engine_speed.png` - Engine speed distribution

## 🔧 API Endpoints

### `GET /`
Returns API information and loaded vehicle data.

### `POST /analyze`
**Main analysis endpoint** - Processes natural language requests.

**Request Example:**
```json
{
  "signal_descriptions": {
    "Eng_nEng10ms": "Engine speed",
    "Eng_uBatt": "Battery voltage in mV", 
    "FuSHp_pRailBnk1": "Fuel Pressure"
  },
  "analysis_description": "Create a histogram of the battery voltage"
}
```

**Response Example:**
```json
{
  "analysis_type": "histogram",
  "description": "Generated histogram analysis for Eng_uBatt using real vehicle data",
  "plot_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
  "statistics": {
    "Vehicle01": {"mean": 12.45, "std": 0.34, "count": 51009},
    "Vehicle03": {"mean": 12.38, "std": 0.41, "count": 26345},
    "Vehicle05": {"mean": 12.52, "std": 0.29, "count": 27009}
  },
  "vehicle_data": {
    "vehicles_analyzed": ["Vehicle01_meas4", "Vehicle03_meas3", "Vehicle05_meas3"],
    "signal_analyzed": "Eng_uBatt",
    "data_source": "Real CSV files from MDF extraction"
  }
}
```

### `GET /available_signals`
Lists all available signals from loaded vehicle data.

## 🎯 Natural Language Processing

The system interprets various analysis requests:

| Request | Detected Analysis | Generated Output |
|---------|------------------|------------------|
| "Create a histogram of battery voltage" | Histogram | Multi-vehicle stacked histogram |
| "Show fuel pressure distribution" | Histogram | Pressure distribution chart |
| "Display engine speed over time" | Time Series | Time-based plot |
| "Compare voltages between vehicles" | Histogram | Comparative analysis |

## 📈 Generated Visualizations

All outputs match IAV Zio Insight styling:
- **Multi-vehicle stacked histograms**
- **Statistical overlays** 
- **Professional automotive color schemes**
- **Proper units and labeling**
- **Vehicle-specific legends**

## 🧪 Testing the Implementation

### Interactive Web Interface
Visit `http://localhost:8000/docs` for Swagger UI testing.

### Command Line Testing
```bash
# Test with curl
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "signal_descriptions": {"Eng_uBatt": "Battery voltage in mV"},
    "analysis_description": "Create a histogram of the battery voltage"
  }'
```

### Python Testing
```python
import requests

response = requests.post("http://localhost:8000/analyze", json={
    "signal_descriptions": {
        "Eng_uBatt": "Battery voltage in mV"
    },
    "analysis_description": "Create a histogram of the battery voltage"
})

result = response.json()
print(f"Analysis: {result['analysis_type']}")
print(f"Vehicles: {len(result['statistics'])}")
```

## 📊 Data Processing Pipeline

1. **CSV Loading**: Automatically loads all vehicle measurement files
2. **Signal Detection**: Identifies requested signals across channel groups  
3. **Analysis Type Recognition**: Interprets natural language descriptions
4. **Multi-Vehicle Processing**: Combines data from all available vehicles
5. **Visualization Generation**: Creates IAV Zio Insight-style plots
6. **Statistics Calculation**: Provides mean, std, min, max for each vehicle
7. **Response Formatting**: Returns base64-encoded plots and structured data

## 🔄 Comparison with IAV Zio Insight

| Feature | IAV Zio Insight | This API |
|---------|-----------------|----------|
| **Input** | Manual GUI operations | Natural language REST requests |
| **Data Loading** | Manual file selection | Automatic CSV processing |
| **Analysis Types** | Pre-defined templates | AI-interpreted descriptions |
| **Output Format** | Static images | Base64 + JSON with statistics |
| **Integration** | Desktop application | REST API for any system |
| **Automation** | Manual workflow | Fully automated |

## 🎉 Task Completion Verification

Run the complete verification:
```bash
# 1. Start server
python run_server.py

# 2. Run task demonstration
python task_demo.py
```

**Expected Success Output:**
```
🎉 ALL TASK REQUIREMENTS COMPLETED SUCCESSFULLY!
   ✅ IAV Zio Insight functionality successfully replaced
   ✅ Natural language analysis requests working
   ✅ Multi-vehicle histograms generated
   ✅ Statistics calculated for all vehicles
   ✅ Automotive signals correctly processed
```

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (when server running)
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

## 🔧 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in run_server.py or use environment variable
export API_PORT=8001
python run_server.py
```

**No CSV data found:**
- Ensure CSV files are in `data/csv/` directory
- Check file naming: `Vehicle##_meas#.ChannelGroup_#.csv`

**matplotlib GUI errors:**
- The code uses non-interactive backend (`Agg`)
- All plots are saved as files, no GUI required
