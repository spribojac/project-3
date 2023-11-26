// Fetch data from your Flask API route
d3.json("static/spotify_songs.json").then((data) => {
    // Extract playlist_genre data
    const playlistGenres = data.map(entry => entry.playlist_genre);
    // Count occurrences of each playlist_genre
    const playlistGenreCounts = playlistGenres.reduce((acc, genre) => {
        acc[genre] = (acc[genre] || 0) + 1;
        return acc;
    }, {});
    // Create an array for Plotly pie chart
    const pieData = [{
        labels: Object.keys(playlistGenreCounts),
        values: Object.values(playlistGenreCounts),
        type: "pie"
    }];
    const layout = {
        title: "Playlist Genre Distribution"
    };
    // Plot the chart to a div tag with an ID of "pieplot".
    Plotly.newPlot("pieplot", pieData, layout);
});