document.getElementById('scrapeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const contestName = document.getElementById('contestName').value;
    fetch(`/scrape?contestName=${encodeURIComponent(contestName)}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('results').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('results').innerHTML = '<p>Error loading data.</p>';
        });
});
