import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import requests

def get_bricks_from_github(repo_url, file_path):
    """
    Fetches a CSV file from a public GitHub repository and returns its data as a pandas DataFrame.

    Args:
        repo_url (str): The URL of the GitHub repository.
        file_path (str): The path to the CSV file within the repository.

    Returns:
        pd.DataFrame: A DataFrame containing the CSV data.
    """
    # Construct the raw content URL for the file
    raw_url = f"{repo_url}/raw/main/{file_path}"

    try:
        # Send a GET request to the raw content URL
        response = requests.get(raw_url)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # Read the content of the response into a pandas DataFrame
        df = pd.read_csv(io.StringIO(response.text))
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub: {e}")
        return None

if __name__ == "__main__":
    # --- Instructions for you to modify ---
    # 1. Replace the placeholder URL with the URL of your own public GitHub repository.
    #    Make sure the URL points to the repository, not a specific file or folder.
    # 2. Update the 'file_path' variable to match the path of your CSV file within the repo.
    #
    # Example for a repository at https://github.com/your_username/your_repo:
    # repo_url = "https://github.com/your_username/your_repo"
    # file_path = "bricks_layout.csv" # If the file is in the root directory

    # Placeholder for demonstration
    # Replace with your actual repository URL and file path
    repo_url = "https://github.com/Parth-Shrivastava/TerafacTechnologies"
    file_path = "bricks_layout.csv"




    # Get the data from GitHub
    bricks_df = get_bricks_from_github(repo_url, file_path)

    if bricks_df is not None:
        # Create a 3D scatter plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Plot the brick locations
        ax.scatter(bricks_df['x'], bricks_df['y'], bricks_df['z'], s=5, c='blue')

        # Set labels for the axes
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Set title
        ax.set_title('3D Scatter Plot of Brick Locations')

        # Save the plot to a file
        plt.savefig('bricks_3d_scatter_plot.png')
        plt.show()

        print("3D scatter plot generated and saved as 'bricks_3d_scatter_plot.png'")