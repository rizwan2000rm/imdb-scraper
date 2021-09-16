from bs4 import BeautifulSoup
import requests

IMDB_LINK = "https://www.imdb.com/chart/top"
LINK_PREFIX = "https://www.imdb.com/"


class Movies:
    def __init__(self):
        self.movies = {}

    def fetchMovies(self, count):
        topMoviesPage = requests.get(IMDB_LINK)  # *Get the HTML Page*
        topMoviesSoup = BeautifulSoup(
            topMoviesPage.content, 'html.parser')  # *Create a soup

        # *Create a hashmap storing movies data => O(count)*
        for idx, element in enumerate(topMoviesSoup.select('.titleColumn a')):
            if idx == count:
                break

            self.movies[idx] = {
                "id": idx,
                "title": element.text,
                "credits-href": element.get('href') + "fullcredits",
            }

        # *Fetch casts for all movies add it to the hashmap => O(N)*
        for idx, movie in self.movies.items():
            if idx == count:
                break
            castsPage = requests.get(LINK_PREFIX + movie["credits-href"])
            movieCastSoup = BeautifulSoup(castsPage.content, 'html.parser')
            casts = set()
            for cast in movieCastSoup.select(".cast_list tr td:nth-child(2) a"):
                casts.add(cast.text.strip())
            movie["casts"] = casts

    def printMovies(self):
        print(self.movies)

    def getMoviesFromActors(self, actor, count):
        movies = []
        resultCount = 0
        for idx, movie in self.movies.items():
            if resultCount == count:
                break
            if actor in movie["casts"]:
                movies.append(movie)
                resultCount += 1
        print("movies", movies)


def main():
    movies = Movies()
    movies.fetchMovies(3)
    # movies.printMovies()
    movies.getMoviesFromActors("Al Pacino", 2)


main()
