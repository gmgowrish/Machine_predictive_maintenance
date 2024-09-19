import pandas as pd
from myapp.modules.model import failure_type, is_failure
import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render, redirect
from django.http import FileResponse
from django.urls import reverse

def index(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        with open('uploaded/input.csv', 'wb') as f:
            f.write(uploaded_file.read())

        df = pd.read_csv('uploaded/input.csv')
        df['is_failure'] = is_failure(df)
        df['failure_type'] = failure_type(df)
        df_filtered = df[df['is_failure'] == 1]
        df_filtered.to_csv('uploaded/output.csv', index=False)

        response = FileResponse(open('uploaded/output.csv', 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=output.csv'
        return redirect(reverse('report'))
    
    return render(request, 'index.html')

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from django.shortcuts import render

def report(request):
    # Read input.csv
    try:
        input_df = pd.read_csv('uploaded/input.csv')
    except FileNotFoundError:
        return render(request, 'report.html', {'error': 'Input file not found'})

    # Read output.csv
    try:
        output_df = pd.read_csv('uploaded/output.csv')
    except FileNotFoundError:
        return render(request, 'report.html', {'error': 'Output file not found'})

    # Verify columns in input_df
    input_columns = input_df.columns.tolist()
    output_columns = output_df.columns.tolist()

    # Print columns for debugging
    print("Input Columns:", input_columns)
    print("Output Columns:", output_columns)

    # Define numeric columns
    numeric_columns = ['Air temperature [K]', 'Process temperature [K]', 
                        'Rotational speed [rpm]', 'Torque [Nm]', 'Tool wear [min]']

    # Ensure 'Type' column exists
    if 'Type' not in input_columns:
        return render(request, 'report.html', {'error': 'Missing column: Type in input data'})

    # Ensure 'Type' column values are categorical
    input_df['Type'] = input_df['Type'].astype('category')
    output_df['Type'] = output_df['Type'].astype('category')

    # Convert columns to numeric where applicable
    input_df[numeric_columns] = input_df[numeric_columns].apply(pd.to_numeric, errors='coerce')
    output_df[numeric_columns] = output_df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Generate interactive bar plot for input data
    if 'Type' in input_columns:
        input_bar_fig = px.bar(input_df, x='Type', title="Distribution of Type in Input Data",
                            labels={"Type": "Type", "count": "Frequency"},
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        input_bar_html = input_bar_fig.to_html(full_html=False)
    else:
        input_bar_html = "<p>Error: 'Type' column missing in input data.</p>"

    # Generate interactive pie plot for input data
    if 'Type' in input_columns:
        input_pie_fig = px.pie(input_df, names='Type', title="Distribution of Type in Input Data",
                            labels={"Type": "Type"},
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        input_pie_html = input_pie_fig.to_html(full_html=False)
    else:
        input_pie_html = "<p>Error: 'Type' column missing in input data.</p>"

    # Generate 3D scatter plot for input data
    input_scatter3d_fig = go.Figure(data=[go.Scatter3d(
        x=input_df['Rotational speed [rpm]'],
        y=input_df['Torque [Nm]'],
        z=input_df['Tool wear [min]'],
        mode='markers',
        marker=dict(
            size=5,
            color=input_df['Type'].cat.codes,  # Use numeric codes for color
            opacity=0.8
        )
    )])
    input_scatter3d_fig.update_layout(
        title="3D Scatter Plot of Input Data",
        scene=dict(
            xaxis_title='Rotational speed [rpm]',
            yaxis_title='Torque [Nm]',
            zaxis_title='Tool wear [min]'
        )
    )
    input_scatter3d_html = input_scatter3d_fig.to_html(full_html=False)

    # Generate interactive bar plot for output data
    if 'Type' in output_columns:
        output_bar_fig = px.bar(output_df, x='Type', title="Distribution of Type in Output Data",
                            labels={"Type": "Type", "count": "Frequency"},
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        output_bar_html = output_bar_fig.to_html(full_html=False)
    else:
        output_bar_html = "<p>Error: 'Type' column missing in output data.</p>"

    # Generate interactive pie plot for output data
    if 'Type' in output_columns:
        output_pie_fig = px.pie(output_df, names='Type', title="Distribution of Type in Output Data",
                            labels={"Type": "Type"},
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        output_pie_html = output_pie_fig.to_html(full_html=False)
    else:
        output_pie_html = "<p>Error: 'Type' column missing in output data.</p>"

    # Generate 3D scatter plot for output data
    output_scatter3d_fig = go.Figure(data=[go.Scatter3d(
        x=output_df['Rotational speed [rpm]'],
        y=output_df['Torque [Nm]'],
        z=output_df['Tool wear [min]'],
        mode='markers',
        marker=dict(
            size=5,
            color=output_df['Type'].cat.codes,  # Use numeric codes for color
            opacity=0.8
        )
    )])
    output_scatter3d_fig.update_layout(
        title="3D Scatter Plot of Output Data",
        scene=dict(
            xaxis_title='Rotational speed [rpm]',
            yaxis_title='Torque [Nm]',
            zaxis_title='Tool wear [min]'
        )
    )
    output_scatter3d_html = output_scatter3d_fig.to_html(full_html=False)

    # Generate line charts for input and output data
    input_line_fig = px.line(input_df, x='Rotational speed [rpm]', y=['Torque [Nm]', 'Tool wear [min]'],
                             title="Line Chart of Input Data",
                             labels={"value": "Values", "variable": "Features"},
                             markers=True)
    input_line_html = input_line_fig.to_html(full_html=False)

    output_line_fig = px.line(output_df, x='Rotational speed [rpm]', y=['Torque [Nm]', 'Tool wear [min]'],
                              title="Line Chart of Output Data",
                              labels={"value": "Values", "variable": "Features"},
                              markers=True)
    output_line_html = output_line_fig.to_html(full_html=False)

    # Generate scatter charts for input and output data
    input_scatter_fig = px.scatter(input_df, x='Rotational speed [rpm]', y='Torque [Nm]', color='Type',
                                   title="Scatter Chart of Input Data",
                                   labels={"Rotational speed [rpm]": "Rotational Speed [rpm]", "Torque [Nm]": "Torque [Nm]"},
                                   trendline="ols")  # Ensure statsmodels is installed
    input_scatter_html = input_scatter_fig.to_html(full_html=False)

    output_scatter_fig = px.scatter(output_df, x='Rotational speed [rpm]', y='Torque [Nm]', color='Type',
                                    title="Scatter Chart of Output Data",
                                    labels={"Rotational speed [rpm]": "Rotational Speed [rpm]", "Torque [Nm]": "Torque [Nm]"},
                                    trendline="ols")  # Ensure statsmodels is installed
    output_scatter_html = output_scatter_fig.to_html(full_html=False)

    # Generate heatmaps for input and output data
    # Only consider numeric columns for correlation
    input_corr = input_df[numeric_columns].corr()
    input_heatmap_fig = px.imshow(input_corr, text_auto=True, aspect="auto",
                                  title="Heatmap of Input Data Correlations")
    input_heatmap_html = input_heatmap_fig.to_html(full_html=False)

    output_corr = output_df[numeric_columns].corr()
    output_heatmap_fig = px.imshow(output_corr, text_auto=True, aspect="auto",
                                   title="Heatmap of Output Data Correlations")
    output_heatmap_html = output_heatmap_fig.to_html(full_html=False)

    # Generate failure distribution chart
    if 'Failure Type' in output_columns:
        failure_fig = px.pie(output_df, names='Failure Type', title="Failure Distribution",
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        failure_html = failure_fig.to_html(full_html=False)
    else:
        failure_html = "<p>Error: 'Failure Type' column missing in output data.</p>"

    # Pass all figures to context
    context = {
        'input_bar_plot': input_bar_html,
        'input_pie_plot': input_pie_html,
        'input_scatter3d_plot': input_scatter3d_html,
        'output_bar_plot': output_bar_html,
        'output_pie_plot': output_pie_html,
        'output_scatter3d_plot': output_scatter3d_html,
        'input_line_chart': input_line_html,
        'output_line_chart': output_line_html,
        'input_scatter_chart': input_scatter_html,
        'output_scatter_chart': output_scatter_html,
        'input_heatmap': input_heatmap_html,
        'output_heatmap': output_heatmap_html,
        'failure_distribution': failure_html,
    }

    return render(request, 'report.html', context)
