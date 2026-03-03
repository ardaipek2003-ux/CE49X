import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def extract_stations(geojson_path):
    with open(geojson_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    stations = []
    for feature in data['features']:
        props = feature.get('properties', {})
        geom = feature.get('geometry', {})
        
        # Extract brand
        brand = props.get('brand', props.get('name', props.get('operator', 'Unknown')))
        if brand is None: brand = 'Unknown'
        
        # Normalize brand names for consistency
        brand_lower = brand.lower()
        if 'shell' in brand_lower: brand = 'Shell'
        elif 'opet' in brand_lower: brand = 'Opet'
        elif 'petrol ofisi' in brand_lower or 'po' == brand_lower: brand = 'Petrol Ofisi'
        elif 'bp' in brand_lower: brand = 'BP'
        elif 'aytemiz' in brand_lower: brand = 'Aytemiz'
        elif 'total' in brand_lower: brand = 'TotalEnergies'
        elif 'türkiye petrolleri' in brand_lower or 'tp' == brand_lower: brand = 'TP'
        elif 'socar' in brand_lower: brand = 'SOCAR'
        elif 'alpet' in brand_lower: brand = 'Alpet'
        elif 'lukoil' in brand_lower: brand = 'Lukoil'
        
        # Extract coordinates
        if geom['type'] == 'Point':
            lon, lat = geom['coordinates']
        elif geom['type'] in ['Polygon', 'MultiPolygon']:
            # Take centroid of the first ring
            coords = geom['coordinates'][0] if geom['type'] == 'Polygon' else geom['coordinates'][0][0]
            lon = np.mean([c[0] for c in coords])
            lat = np.mean([c[1] for c in coords])
        else:
            continue
            
        stations.append({
            'brand': brand,
            'lat': lat,
            'lon': lon
        })
    
    return pd.DataFrame(stations)

def plot_stations(df, output_path):
    plt.figure(figsize=(15, 10))
    
    # Define colors for major brands
    brand_colors = {
        'Shell': '#ff0000',      # Red
        'Opet': '#00529b',       # Blue
        'Petrol Ofisi': '#d71920',# Red
        'BP': '#009d3d',         # Green
        'Aytemiz': '#f7941e',    # Orange
        'TotalEnergies': '#00a19a',# Teal
        'TP': '#e30613',         # Red
        'SOCAR': '#0067b1',      # Blue
        'Unknown': '#808080'     # Gray
    }
    
    # Get top brands for the legend
    top_brands = df['brand'].value_counts().head(8).index.tolist()
    
    for brand in df['brand'].unique():
        brand_df = df[df['brand'] == brand]
        color = brand_colors.get(brand, '#000000') # Default black for others
        label = brand if brand in top_brands else None
        
        plt.scatter(brand_df['lon'], brand_df['lat'], 
                    c=color, label=label, s=20, alpha=0.7, edgecolors='none')
    
    plt.title('Gas Stations in Istanbul (from OpenStreetMap)', fontsize=16)
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Add a custom legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title='Major Brands', loc='upper right')
    
    # Set reasonable limits for Istanbul
    plt.xlim(28.0, 29.8)
    plt.ylim(40.8, 41.5)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"Map saved to {output_path}")

if __name__ == "__main__":
    geojson_path = r'C:\Users\arda\Documents\CE49X\Week03_NumPy_Pandas\lab\export.geojson'
    output_path = r'C:\Users\arda\Documents\CE49X\Week03_NumPy_Pandas\lab\istanbul_gas_stations_map.png'
    
    print("Extracting station data...")
    df = extract_stations(geojson_path)
    print(f"Found {len(df)} stations.")
    
    print("Generating map...")
    plot_stations(df, output_path)
    
    # Print some stats
    print("\nBrand Distribution:")
    print(df['brand'].value_counts().head(10))
