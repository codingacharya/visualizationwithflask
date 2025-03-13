from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    graph_html = None
    columns = []
    
    if request.method == "POST":
        file = request.files["file"]
        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)

            df = pd.read_csv(file_path)
            columns = df.columns.tolist()

            # Create a beautiful scatter plot
            fig = px.scatter(df, x=df.columns[0], y=df.columns[1], color=df.columns[2] if len(df.columns) > 2 else None, 
                             title="Scatter Plot", color_continuous_scale="rainbow")
            graph_html = fig.to_html(full_html=False)

            

    return render_template("index.html", graph_html=graph_html, columns=columns)


@app.route("/heatmap")
def heatmap():
    file_path = "uploads/sample.csv"  # Replace with your dataset
    df = pd.read_csv(file_path)
    
    fig = px.imshow(df.corr(), color_continuous_scale="Viridis", title="Heatmap")
    return fig.to_html(full_html=False)

@app.route("/bar")
def bar_chart():
    file_path = "uploads/sample.csv"
    df = pd.read_csv(file_path)
    
    fig = px.bar(df, x=df.columns[0], y=df.columns[1], color=df.columns[2] if len(df.columns) > 2 else None,
                 title="Bar Chart", color_continuous_scale="Bluered")
    return fig.to_html(full_html=False)


if __name__ == "__main__":
    app.run(debug=True)
