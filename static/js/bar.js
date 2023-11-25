// Fetch data from your Flask API route
d3.json("static/spotify_songs.json").then((data) => {
    console.log(data);
    // Extract playlist_genre data
    const playlistGenres = data.map(entry => entry.playlist_genre);
    // Create an object to store counts for each category
    const categoryCounts = {};
    // Loop through each category and calculate counts
    const categories = ["danceability", "energy", "loudness", "speechiness", "acousticness", "liveness", "valence", "tempo", "instrumentalness",]
    categories.forEach(category => {
        categoryCounts[category] = data.reduce((acc, entry) => {
            const genre = entry.playlist_genre;
            const value = entry[category];
            acc[genre] = acc[genre] || {};
            acc[genre][category] = (acc[genre][category] || 0) + value;
            return acc;
        }, {});
    });
    // Populate the dropdown menu for categories
    const dropdown = d3.select("#categoryDropdown");
    // Add an event listener to the dropdown to update the bar chart based on the selected category
    dropdown.on("change", function () {
        const selectedCategory = this.value;
        // Calculate counts for each genre based on the selected category
        const genreCounts = categoryCounts[selectedCategory];
        // Create bar data for the selected category
        const barData = Object.keys(genreCounts).map(genre => ({
            x: [genre],
            y: [genreCounts[genre][selectedCategory]],  // Use the selectedCategory for the y value
            type: "bar",
            name: genre
        }));
        const layout = {
            title: `${selectedCategory} Distribution by Genre`,
            xaxis: {
                title: "Genre"
            },
            yaxis: {
                title: selectedCategory
            }
        };
        // Create a div for the bar chart
        const divId = `${selectedCategory}BarPlot`;
        const existingDiv = document.getElementById(divId);
        // If the div already exists, update the existing chart
        if (existingDiv) {
            Plotly.newPlot(divId, barData, layout);
        } else {
            // If the div doesn't exist, create a new div and plot the chart
            document.getElementById("bar-container").innerHTML += `<div id="${divId}"></div>`;
            Plotly.newPlot(divId, barData, layout);
        }
    });
});