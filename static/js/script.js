function main(){
  let years = null;
  let papers_per_years = null;

  let url='/getpq'

  const request = new XMLHttpRequest();
  request.open('GET', url, false);  // `false` makes the request synchronous
  request.send(null);

  if (request.status === 200) {
    let response_json = JSON.parse(request.responseText);
    console.log(response_json);
    years = response_json['years'];
    papers_per_years = response_json['publications'];
  }

  var data = [
    {
      x: years,
      y: papers_per_years,
      type: 'bar'
    }
  ];

  Plotly.newPlot('bar_plot', data);
}
