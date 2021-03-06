dir <- "/Users/jtimmons/Documents/GitHub/ff/data/historical"
setwd(dir)

sources <- list(
  list(
    source = "CBS",
    name = "name",
    pts = "pts_cbs",
    years = c(2012, 2013)
  ),
  list(
    source = "CBS",
    name = "name_cbs",
    pts = "pts_cbs",
    years = c(2014)
  ),
  list(
    source = "FOX",
    name = "name_fox",
    pts = "pts_fox",
    years = c(2014)
  ),
    list(
    source = "ESPN",
    name = "name",
    pts = "pts_espn",
    years = c(2012, 2013)
  ),
  list(
    source = "ESPN",
    name = "name_espn",
    pts = "pts_espn",
    years = c(2014)
  ),
  list(
    source = "NFL",
    name = "name",
    pts = "pts_nfl",
    years = c(2012, 2013)
  ),
  list(
    source = "NFL",
    name = "name_nfl",
    pts = "pts_nfl",
    years = c(2014)
  ),
  list(
    source = "Yahoo",
    name = "name_yahoo",
    pts = "pts_yahoo",
    years = c(2014)
  )
)

year.names <- c()
for (src in sources) {
  for (year in src$years) {
    hist.data.path <- paste0(dir, "/", src$source, "-Projections-", year, ".RData")
    d <- load(hist.data.path)
    fr <- get(d)
    fr <- fr[!duplicated(fr[src$name]),]

    # create the column
    col.name <- paste0(tolower(src$source), ".", year)
    year.names <- c(year.names, col.name)
    player.data[, col.name] <- NA

    # get names and points out of the data frame
    source.data <- data.frame(name = fr[, src$name], year = rep(year, nrow(fr)))
    source.data[col.name] <- fr[, paste0("pts_", tolower(src$source))]

    # add the point values in player.data
    player.data <- merge(player.data, source.data, by = c("name", "year"), all.x = TRUE)
    player.data[col.name] <- player.data[, paste0(col.name, ".y")]
    player.data[paste0(col.name, ".x")] <- NULL
    player.data[paste0(col.name, ".y")] <- NULL
  }
}

# only 2012-2014
player.data <- player.data[player.data$year %in% c(2012, 2013, 2014),]
player.data$experts <- apply(player.data[, year.names], 1, function(x) mean(x, na.rm = TRUE))
