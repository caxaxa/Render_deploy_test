import numpy as np
import plotly.graph_objects as go
from scipy.stats import norm, lognorm
import panel as pn
import markdown
import base64


# Defining functions to open images and markdown inside the html
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def read_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return markdown.markdown(content)
    
#setting the html content

content_html = f"""
    <div style="max-width: 80%; margin-left: auto; margin-right: auto; font-family: Arial, sans-serif; font-size: 22px; line-height: 1.5; color: #333; word-wrap: break-word;">
        <div style="margin-bottom: 20px;">{read_content('Data/content1.txt')}</div>
        <img src="{f"data:image/png;base64,{encode_image('Data/fig1.png')}"}" style="width: 66%; height: auto; display: block; margin: 20px auto;" />
        <div style="margin-bottom: 20px;">{read_content('Data/content2.txt')}</div>
        <img src="{f"data:image/png;base64,{encode_image('Data/fig2.png')}"}" style="width: 120%; height: auto; display: block; margin: 20px auto;" />
        <div style="margin-bottom: 20px;">{read_content('Data/content3.txt')}</div>
        <img src="{f"data:image/png;base64,{encode_image('Data/fig3.png')}"}" style="width: 120%; height: auto; display: block; margin: 20px auto;" />
        <div style="margin-bottom: 20px;">{read_content('Data/content4.txt')}</div>
        <img src="{f"data:image/png;base64,{encode_image('Data/fig4.png')}"}" style="width: 120%; height: auto; display: block; margin: 20px auto;" />
        <div style="margin-bottom: 20px;">{read_content('Data/content5.txt')}</div>
    </div>
    """ 


# Include your custom CSS
css = """
.center-content {
    max-width: 80%;
    margin: 0 auto; /* Center the content horizontally */
    padding: 20px;
}
.center-content .bk.markdown { /* Targeting Markdown content specifically */
    margin-left: 10cm;
    margin-right: 10cm;
}

.center-content img {
    width: 100%;
    max-width: 50%;
    height: auto;
    display: block;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 20px;
}

.custom-font {
    font-family: 'Arial', sans-serif;
    font-size: 22px;
    line-height: 1.5;
    color: #333;
}
"""

pn.extension(raw_css=[css])


def read_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def scaled_image(path, scale=0.5):
    # Read the image to determine its size
    from PIL import Image
    image = Image.open(path)
    width, _ = image.size
    
    # Scale the width
    scaled_width = int(width * scale)
    
    return pn.pane.PNG(path, width=scaled_width)


class Dashboard:
    def __init__(self, df_1, df_2, CV_dict):
        self.dfs = {'Google Ads': df_1, 'Meta Ads': df_2}
        self.df = df_1
        self.columns = ['Cost Per Click', 'Cost Per Lead', 'Click Through Rate', 'Conversion Rate', 'Average ROAS']
        self.CV_dict = CV_dict
        self.setup_dashboard()

    def setup_dashboard(self):
        self.select_widget = pn.widgets.Select(name='Select Ads Platform', options=['Google Ads', 'Meta Ads'])
        self.industry_widget = pn.widgets.Select(name='Select Industry', options=self.get_industries(self.df))
        self.dropdown = pn.widgets.Select(name='Select Metric', options=self.columns)
        self.selected_plot = pn.pane.Plotly()
        self.select_widget.param.watch(self.change_df, 'value')
        self.industry_widget.param.watch(self.update_selected_plot, 'value')
        self.dropdown.param.watch(self.update_selected_plot, 'value')
        self.dropdown.value = self.columns[0]
        self.industry_widget.value = self.get_industries(self.df)[0]

    def change_df(self, event):
        self.df = self.dfs[event.new]
        self.industry_widget.options = self.get_industries(self.df)
        self.update_selected_plot(None)

    def update_selected_plot(self, event):
        selected_option = self.dropdown.value
        industry = self.industry_widget.value
        selected_row = self.df[self.df['Industry'] == industry].iloc[0]
        if selected_option in ['Cost Per Click', 'Cost Per Lead']:
          self.selected_plot.object = self.plot_selected_ranks_1(industry, selected_option, selected_row[selected_option], selected_row[selected_option]*self.CV_dict[selected_option])
        else:
          self.selected_plot.object = self.plot_selected_ranks_2(industry, selected_option, selected_row[selected_option], selected_row[selected_option]*self.CV_dict[selected_option])

    def plot_selected_ranks_1(self, industry, name, mean, std=None):
      dist = norm(loc=mean, scale=std)
      x = np.linspace(0,dist.ppf(0.999), 1000)
      y = dist.pdf(x)*mean
      quartiles = [dist.ppf(q) for q in [0.25, 0.50, 0.75, 1.00]]

      fig = go.Figure()
      fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))

      colors = ['rgba(0, 255, 0, 0.5)', 'rgba(0, 0, 255, 0.5)', 'rgba(255, 255, 0, 0.5)', 'rgba(255, 0, 0, 0.5)']
      labels = ['Master', 'Expert', 'Professional', 'Contributor']
      for i in range(4):
          if i == 0:
              mask = x < quartiles[i]
          else:
              mask = (x >= quartiles[i-1]) & (x < quartiles[i])
          fig.add_trace(go.Scatter(x=x[mask], y=y[mask], fill='tozeroy',
                                  fillcolor=colors[i], line_color='rgba(0,0,0,0)',
                                  name=labels[i], hoverinfo='skip'))

      fig.update_layout(
          title='Distribution of {} - {}'.format(name, industry),
          xaxis_title='Values',
          yaxis_title='Probability',
          yaxis=dict(range=[0, 1])
  )
      fig.update_xaxes(autorange=True)
      return fig


    def plot_selected_ranks_2(self, industry, name, mean, std=None):
      dist = lognorm(s=1, loc=mean/2, scale=std)

      x = np.linspace(0,dist.ppf(0.999), 1000)
      y = dist.pdf(x)*(mean/2)
      quartiles = [dist.ppf(q) for q in [0.25, 0.50, 0.75, 1.00]]

      fig = go.Figure()
      fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))

      colors = [ 'rgba(255, 0, 0, 0.5)', 'rgba(255, 255, 0, 0.5)' ,'rgba(0, 0, 255, 0.5)','rgba(0, 255, 0, 0.5)']
      labels = [ 'Contributor','Professional','Expert','Master']
      for i in range(4):
          if i == 0:
              mask = x < quartiles[i]
          else:
              mask = (x >= quartiles[i-1]) & (x < quartiles[i])
          fig.add_trace(go.Scatter(x=x[mask], y=y[mask], fill='tozeroy',
                                  fillcolor=colors[i], line_color='rgba(0,0,0,0)',
                                  name=labels[i], hoverinfo='skip'))

      fig.update_layout(
          title='Distribution of {} - {}'.format(name, industry),
          xaxis_title='Values',
          yaxis_title='Probability',
          yaxis=dict(range=[0, 1])
  )
      fig.update_xaxes(autorange=True)
      return fig
    def get_dashboard(self):
        content = pn.Column(
                    pn.pane.HTML(content_html, width=800, height= 4600),
                    pn.pane.Markdown('# Discover your Rank'),
                    pn.Row(self.select_widget, self.dropdown, self.industry_widget, margin=(0, 20)),
                    self.selected_plot,
                    pn.pane.Markdown('### Meta Ads National Averages'),
                    pn.pane.DataFrame(self.dfs['Meta Ads']),
                    pn.pane.Markdown('### Google Ads National Averages'),
                    pn.pane.DataFrame(self.dfs['Google Ads']),
                )
        return pn.Row(content)

    def save_dashboard(self, filename):
        self.get_dashboard().save(filename, embed=True)

    @staticmethod
    def get_industries(df):
        return df['Industry'].unique().tolist()


