const fs = require('fs');
const readline = require('readline');
let jsonObjectArr = [];

async function processLineByLine() {
    const fileStream = fs.createReadStream('./data.jsonl');

    const rl = readline.createInterface({
        input: fileStream,
        crlfDelay: Infinity
    });

    for await (const line of rl) {
        // Parse JSON line and push to array
        try {
            jsonObjectArr.push(JSON.parse(line));
        } catch (error) {
            console.error('Error parsing JSON line:', error);
        }
    }
    console.log(jsonObjectArr);
}

processLineByLine();