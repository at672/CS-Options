import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import argparse
import os

def prepare_surface_data(csv_file):
    """
    Load and prepare the CSV data for 3D plotting.
    """
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Convert tenor strings to numeric values (assuming format like '1Y', '2Y', etc.)
    tenors = df['Tenor/Strike'].str.replace('Y', '').astype(float)
    
    # Convert strike rate strings to numeric values
    strikes = pd.to_numeric(df.columns[1:].str.rstrip('%').str.replace('ATM', '0'), errors='coerce')
    
    # Create meshgrid for 3D surface
    X, Y = np.meshgrid(strikes, tenors)
    
    # Convert volatility values to numeric array
    Z = df.iloc[:, 1:].astype(float).values
    
    return X, Y, Z, strikes, tenors

def create_surface_plot(csv_file, output_file, dpi=300, figsize=(16, 12)):
    """
    Create a high-resolution 3D surface plot of the volatility surface.
    """
    # Prepare data
    X, Y, Z, strikes, tenors = prepare_surface_data(csv_file)
    
    # Set style
    plt.style.use('seaborn')
    
    # Create figure with high DPI
    fig = plt.figure(figsize=figsize, dpi=dpi)
    ax = fig.add_subplot(111, projection='3d')
    
    # Create surface plot with custom colormap
    surf = ax.plot_surface(X, Y, Z, 
                          cmap='viridis',
                          linewidth=0.5,
                          antialiased=True,
                          alpha=0.8)
    
    # Customize the plot
    ax.set_xlabel('Strike (%)', fontsize=12, labelpad=10)
    ax.set_ylabel('Tenor (Years)', fontsize=12, labelpad=10)
    ax.set_zlabel('Volatility', fontsize=12, labelpad=10)
    
    # Set title with larger font
    plt.title('Interest Rate Volatility Surface', fontsize=16, pad=20)
    
    # Add color bar
    cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Volatility Level', fontsize=10)
    
    # Set viewing angle
    ax.view_init(elev=30, azim=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save high-resolution figure
    plt.savefig(output_file, 
                dpi=dpi, 
                bbox_inches='tight',
                pad_inches=0.5)
    
    plt.close()

def plot_all_angles(csv_file, output_folder, angles=[(0, 0), (90, 0), (45, 180), (60, 270)], 
                    dpi=300, figsize=(16, 12)):
    """
    Create multiple views of the surface from different angles.
    """
    X, Y, Z, strikes, tenors = prepare_surface_data(csv_file)
    
    for elev, azim in angles:
        # Create new figure for each angle
        plt.style.use("seaborn-v0_8-whitegrid")
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.add_subplot(111, projection='3d')
        
        # Create surface plot
        surf = ax.plot_surface(X, Y, Z, 
                             cmap='viridis',
                             linewidth=0.5,
                             antialiased=True,
                             alpha=0.8)
        
        # Customize the plot
        ax.set_xlabel('Strike (%)', fontsize=12, labelpad=10)
        ax.set_ylabel('Tenor (Years)', fontsize=12, labelpad=10)
        ax.set_zlabel('Volatility', fontsize=12, labelpad=10)
        
        plt.title(f'Volatility Surface (elev={elev}°, azim={azim}°)', fontsize=16, pad=20)
        
        # Add color bar
        cbar = fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label('Volatility Level', fontsize=10)
        
        # Set viewing angle
        ax.view_init(elev=elev, azim=azim)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        base_name = os.path.splitext(os.path.basename(csv_file))[0]
        plt.savefig(f'{output_folder}/{base_name}_elev{elev}_azim{azim}.png', 
                    dpi=dpi, 
                    bbox_inches='tight',
                    pad_inches=0.5)
        
        plt.close()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create 3D volatility surface plots')
    parser.add_argument('csv_file', type=str, help='Path to the CSV file containing volatility surface data')
    parser.add_argument('--output-dir', type=str, default='surface_plots',
                        help='Directory to save the plots (default: surface_plots)')
    parser.add_argument('--dpi', type=int, default=300,
                        help='DPI for output images (default: 300)')
    parser.add_argument('--figsize', type=float, nargs=2, default=[16, 12],
                        help='Figure size in inches (width height) (default: 16 12)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Plot the surface from different angles
    plot_all_angles(args.csv_file, args.output_dir, dpi=args.dpi, figsize=tuple(args.figsize))
    
    # Create a single main view
    base_name = os.path.splitext(os.path.basename(args.csv_file))[0]
    output_file = os.path.join(args.output_dir, f'{base_name}_main.png')
    create_surface_plot(args.csv_file, output_file, dpi=args.dpi, figsize=tuple(args.figsize))
    
    print(f"Plots have been saved to the {args.output_dir} directory.")