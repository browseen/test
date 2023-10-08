var dataj = [];

function loadJsonL() {
    let jsonObjectArr = [];

    fetch('data.jsonl')
        .then(response => response.text())
        .then(data => {
            // split data into lines
            const lines = data.split('\n');

            // parse each line into an object and ignore empty lines
            lines.forEach(line => {
                if(line) {
                    try {
                        jsonObjectArr.push(JSON.parse(line));
                    } catch(e) {
                        console.error("Error parsing JSON line:", e);
                    }
                }
            });

            // log objects (replace with your code)
            console.log(jsonObjectArr);
            dataj = jsonObjectArr;
        })
        .catch(err => console.error('Error:', err));
}

function browseen(query) {
    query = query || document.getElementById('query').value.toLowerCase();
    console.log("search", query);
    document.getElementById('query').value = query;
    var results = dataj.filter(function (item) {
        return item.url.toLowerCase().includes(query) || item.description.toLowerCase().includes(query);
        //return item.url.toLowerCase().includes(query) || item.description.toLowerCase().includes(query) || item.tags.some(tag => tag.toLowerCase() === query);
    });
    const resultsContainer = document.getElementById('results');
    resultsContainer.innerHTML = results.map(function (item, i) {
        return `
                <div class="result">
                    <h2><a href="${item.url}">${item.url}</a></h2>
                    <p>${item.description}</p>
                    <div class="tags">${item.tags.map(tag => `<a href="#" onclick="event.preventDefault(); browseen('${tag}')">${tag}</a>`).join(', ')}</div>
                    <img id="resultImage${i}" src="${item.icon_64px_base64}" alt="screenshot of ${item.url}">
                </div>`;
    }).join('');
    results.forEach((item, i) => {
        setTimeout(() => {
           // document.getElementById(`resultImage${i}`).src = item.screenshot_url;
        }, 1700);
    });
}


window.onload = loadJsonL;