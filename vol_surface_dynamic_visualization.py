import pandas as pd
import numpy as np
import plotly.graph_objects as go
import argparse
import os
from pathlib import Path

def prepare_surface_data(csv_file):
    """
    Load and prepare the CSV data for 3D plotting.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert tenor strings to numeric values
    # Use proper regex pattern with raw string
    pattern = r'(\d+)'
    tenors = df['Tenor/Strike'].str.extract(pattern).astype(float).values.flatten()   

    # Get strike values (excluding the Tenor/Strike column and ATM column)
    strikes = df.columns[1:].str.rstrip('%')
    strikes = strikes[strikes != 'ATM'].astype(float).values
    
    # Create meshgrid for 3D surface
    X, Y = np.meshgrid(strikes, tenors)
    
    # Convert volatility values to numeric array

    # Get the column indices excluding ATM
    cols_to_use = [col for col in df.columns[1:] if col != 'ATM']
    Z = df[cols_to_use].astype(float).values
    
    return X, Y, Z, strikes, tenors

def create_interactive_surface(csv_file, output_folder):
    """
    Create an interactive 3D surface plot using Plotly.
    """
    # Prepare data
    X, Y, Z, strikes, tenors = prepare_surface_data(csv_file)
    
    # Create the 3D surface
    fig = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale='viridis',
        hoverinfo='x+y+z',  # Show x, y, and z values on hover
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        hovertemplate="Strike: %{x:.2f}%<br>" +
                      "Tenor: %{y:.1f}Y<br>" +
                      #"Vol: %{z:.2f}%<extra></extra>"
                      "Vol: %{z:.2f} bps<extra></extra>"
    )])
    
    base_name = os.path.splitext(os.path.basename(csv_file))[0]

    # Update the layout
    fig.update_layout(
        title=f'Interactive Volatility Surface {base_name}',
        scene=dict(
            xaxis_title='Strike (%)',
            yaxis_title='Tenor (Years)',
            zaxis_title='Volatility (%)',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        width=1000,
        height=800,
        margin=dict(l=65, r=50, b=65, t=90)
    )
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Save as HTML file for interactive viewing
    html_file = os.path.join(output_folder, f'{base_name}_interactive.html')
    fig.write_html(html_file)
    
    print(f"Interactive plot has been saved to {html_file}")
    
    # Show the plot
    fig.show()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create interactive 3D volatility surface plots')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing volatility surface data')
    parser.add_argument('--output-dir', type=str, default='surface_plots',
                       help='Directory to save the plots (default: surface_plots)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create the interactive surface
    create_interactive_surface(args.csv_file, args.output_dir)