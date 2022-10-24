//var scopusApiKey = process.env.SCOPUSAPIKEY;

// check it--- to secret api key
//require('dotenv').config();

function scopus_get_data(year) {
  let url='https://api.elsevier.com/content/search/scopus\
?apiKey=API_KEY\
&query=TITLE-ABS-KEY(privacy%20AND%20quantification%20AND%20NOT%20proceedings)\
&date='+year;


  const request = new XMLHttpRequest();
  request.open('GET', url, false);  // `false` makes the request synchronous
  request.send(null);

  if (request.status === 200) {
    let response_json = JSON.parse(request.responseText);
    paper_per_year = response_json['search-results']['opensearch:totalResults']
    return paper_per_year
  }
  return null;
}

function main(){
  // Get current year
  max_year = new Date().getFullYear();
  min_year = 2008;
  
  let years = [];
  let papers_per_years = [];
  
  for (let i= min_year; i <= max_year; i++) {
    let paper_per_year = scopus_get_data(i);
    console.log(paper_per_year);
    years.push(i);
    papers_per_years.push(paper_per_year);
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



