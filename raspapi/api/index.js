const express = require("express");
const app = express();
const port = 3000;

app.get("/api/astros-playing", async (req, res) => {
  const scheduledGames = await fetch(
    process.env.API_URL
  );
  const data = await scheduledGames.json();
  if (data.totalGames === 0) {
    res.send({ playing: false });
    return;
  }
  const astrosGame = data.dates[0].games.filter(
    (game) => game.teams.away.team.id === 117 || game.teams.home.team.id === 117
  )[0];
  if (astrosGame.length === 0) {
    res.send({ playing: false });
    return;
  }
  res.send({
    playing: true,
    team: astrosGame.teams.away.team.id === 117 ? "away" : "home",
    game: astrosGame,
  });
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
