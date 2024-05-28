from flask import Flask, render_template_string
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    # Load the iris dataset
    iris = sns.load_dataset('iris')

    # Basic EDA
    describe = iris.describe().to_html()
    species_count = iris['species'].value_counts().to_frame().to_html()

    # Create plots
    plots = []

    # Pairplot
    plt.figure(figsize=(10, 6))
    sns.pairplot(iris, hue='species')
    pairplot_img = io.BytesIO()
    plt.savefig(pairplot_img, format='png')
    pairplot_img.seek(0)
    pairplot_data = base64.b64encode(pairplot_img.getvalue()).decode()
    plots.append(f'<img src="data:image/png;base64,{pairplot_data}" style="width:100%;">')

    # Species count plot
    plt.figure(figsize=(6, 4))
    sns.countplot(data=iris, x='species')
    plt.title('Species Count')
    species_count_img = io.BytesIO()
    plt.savefig(species_count_img, format='png')
    species_count_img.seek(0)
    species_count_data = base64.b64encode(species_count_img.getvalue()).decode()
    plots.append(f'<img src="data:image/png;base64,{species_count_data}" style="width:100%;">')

    # Generate HTML
    html = f"""
    <html>
    <head>
        <title>Iris Dataset EDA</title>
    </head>
    <body>
        <h1>Iris Dataset Exploratory Data Analysis</h1>
        <h2>Summary Statistics</h2>
        {describe}
        <h2>Species Count</h2>
        {species_count}
        <h2>Plots</h2>
        {''.join(plots)}
    </body>
    </html>
    """
    
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
