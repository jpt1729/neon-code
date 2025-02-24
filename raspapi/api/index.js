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
  try {
  const astrosGame = data.dates[0].games.filter(
    (game) => game.teams.away.team.id === 117 || game.teams.home.team.id === 117
  )[0];
  if (astrosGame.length === 0) {
    res.send({ playing: false });
    return;
  }
  if (astrosGame.status.statusCode === "F" || astrosGame.status.abstractGameCode === "F"){
    res.send({ playing: false });
    return;
  }
  res.send({
    playing: true,
    error: false,
    team: astrosGame.teams.away.team.id === 117 ? "away" : "home",
    game: astrosGame,
  });
} catch (err) {
  res.send({error: true, ...err})
}
});



app.listen(port, () => {
  console.log(`Astros App app listening on port ${port}`);
});
