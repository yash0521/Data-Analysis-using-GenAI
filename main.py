from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
import glob
import os

# Set matplotlib to use non-interactive backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import base64

app = FastAPI(title="Automotive Data Analysis API", version="1.0.0")

class AnalysisRequest(BaseModel):
    signal_descriptions: Dict[str, str]
    analysis_description: str

class AnalysisResponse(BaseModel):
    analysis_type: str
    description: str
    plot_base64: Optional[str] = None
    statistics: Optional[Dict[str, Any]] = None
    vehicle_data: Optional[Dict[str, Any]] = None

class DataAnalyzer:
    def __init__(self):
        self.vehicle_data = {}
        self.load_real_csv_data()
        
    def load_real_csv_data(self):
        """Load actual CSV data from data/csv directory"""
        csv_folder = "data/csv"
        if not os.path.exists(csv_folder):
            print(f"Warning: {csv_folder} directory not found!")
            return
            
        csv_files = glob.glob(os.path.join(csv_folder, "*.csv"))
        
        for csv_file in csv_files:
            filename = os.path.basename(csv_file)
            # Parse filename: Vehicle01_meas4.ChannelGroup_0.csv
            parts = filename.replace('.csv', '').split('.')
            if len(parts) >= 2:
                vehicle_id = parts[0]  # Vehicle01_meas4
                channel_group = parts[1]  # ChannelGroup_0
                
                if vehicle_id not in self.vehicle_data:
                    self.vehicle_data[vehicle_id] = {}
                
                try:
                    df = pd.read_csv(csv_file)
                    self.vehicle_data[vehicle_id][channel_group] = df
                    print(f"Loaded {filename}: {len(df)} rows, {len(df.columns)} columns")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    def find_signal_in_data(self, signal_name: str):
        """Find signal across all vehicles and channel groups"""
        results = {}
        
        for vehicle_id, channels in self.vehicle_data.items():
            for channel_group, df in channels.items():
                if signal_name in df.columns:
                    data = df[signal_name].dropna()
                    if len(data) > 0:
                        results[vehicle_id] = {
                            'data': data,
                            'channel_group': channel_group,
                            'timestamps': df.get('timestamps', range(len(data)))
                        }
        
        return results
    
    def identify_analysis_type(self, description: str) -> str:
        """Identify the type of analysis requested"""
        desc_lower = description.lower()
        
        if any(word in desc_lower for word in ['histogram', 'distribution', 'freq']):
            return 'histogram'
        elif any(word in desc_lower for word in ['time', 'series', 'over time']):
            return 'timeseries'
        else:
            return 'histogram'  # default
    
    def extract_signals_from_description(self, description: str, signal_descriptions: Dict[str, str]) -> List[str]:
        """Extract signal names from analysis description"""
        signals = []
        desc_lower = description.lower()
        
        # Check for signals mentioned in description
        for signal_name, signal_desc in signal_descriptions.items():
            if (signal_name.lower() in desc_lower or 
                any(word in desc_lower for word in signal_desc.lower().split())):
                signals.append(signal_name)
        
        # If no signals found, use first signal
        if not signals:
            signals = [list(signal_descriptions.keys())[0]]
        
        return signals
    
    def create_iav_style_histogram(self, signal_name: str) -> tuple:
        """Create IAV Zio Insight style histogram using real data"""
        signal_data = self.find_signal_in_data(signal_name)
        
        if not signal_data:
            # If no real data, return error
            raise ValueError(f"No data found for signal: {signal_name}")
        
        plt.ioff()
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Prepare data for stacked histogram
        all_data = []
        labels = []
        colors = plt.cm.Set3(np.linspace(0, 1, len(signal_data)))
        statistics = {}
        
        for i, (vehicle_id, info) in enumerate(signal_data.items()):
            data = info['data']
            all_data.append(data)
            # Extract vehicle number for cleaner labels
            vehicle_num = vehicle_id.split('_')[0].replace('Vehicle', '')
            label = f"Vehicle{vehicle_num.zfill(2)}"
            labels.append(label)
            
            # Calculate statistics
            statistics[label] = {
                'mean': float(data.mean()),
                'std': float(data.std()),
                'min': float(data.min()),
                'max': float(data.max()),
                'count': int(len(data))
            }
        
        # Create stacked histogram (IAV Zio Insight style)
        ax.hist(all_data, bins=30, label=labels, alpha=0.8, 
                stacked=True, color=colors[:len(all_data)])
        
        # Styling to match IAV Zio Insight
        ax.set_xlabel(f'{signal_name} [{self.get_signal_unit(signal_name)}]')
        ax.set_ylabel('Count')
        ax.set_title(f'{signal_name} Distribution')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        
        # Convert plot to base64
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return plot_base64, statistics
    
    def get_signal_unit(self, signal_name: str) -> str:
        """Get unit for signal based on name"""
        signal_lower = signal_name.lower()
        if 'batt' in signal_lower or 'voltage' in signal_lower:
            return 'V'
        elif 'pressure' in signal_lower or 'prail' in signal_lower:
            return 'MPa'
        elif 'speed' in signal_lower or 'neng' in signal_lower:
            return 'rpm'
        else:
            return ''

# Initialize analyzer with real data
analyzer = DataAnalyzer()

@app.get("/")
async def root():
    return {
        "message": "Automotive Data Analysis API - Task Submission",
        "version": "1.0.0",
        "description": "REST API for generating automotive data analyses using AI",
        "loaded_vehicles": list(analyzer.vehicle_data.keys()),
        "status": "Ready for IAV Zio Insight replacement demo"
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """Generate analysis based on signal descriptions and analysis request"""
    
    try:
        # Extract signals from analysis description
        signals = analyzer.extract_signals_from_description(
            request.analysis_description, 
            request.signal_descriptions
        )
        
        signal_name = signals[0]
        
        # Determine analysis type
        analysis_type = analyzer.identify_analysis_type(request.analysis_description)
        
        # Generate analysis using real data
        plot_base64, statistics = analyzer.create_iav_style_histogram(signal_name)
        
        return AnalysisResponse(
            analysis_type=analysis_type,
            description=f"Generated {analysis_type} analysis for {signal_name} using real vehicle data",
            plot_base64=plot_base64,
            statistics=statistics,
            vehicle_data={
                "vehicles_analyzed": list(analyzer.vehicle_data.keys()),
                "signal_analyzed": signal_name,
                "data_source": "Real CSV files from MDF extraction"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/available_signals")
async def get_available_signals():
    """Get list of available signals from loaded real data"""
    all_signals = set()
    
    for vehicle_id, channels in analyzer.vehicle_data.items():
        for channel_group, df in channels.items():
            all_signals.update(df.columns)
    
    # Remove timestamps and common non-signal columns
    signal_columns = [col for col in all_signals 
                     if col not in ['timestamps'] and not col.startswith('Unnamed')]
    
    return {
        "available_signals": sorted(signal_columns),
        "task_signals": {
            "Eng_nEng10ms": "Engine speed",
            "Eng_uBatt": "Battery voltage in mV", 
            "FuSHp_pRailBnk1": "Fuel Pressure"
        },
        "vehicles_loaded": list(analyzer.vehicle_data.keys()),
        "total_signals": len(signal_columns)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)