import scrapy
import os


base_url = 'http://audiobookbay.nl/audio-books/type/'
single_book_url = 'http://audiobookbay.nl/audio-book/'
number_of_pages = 10
genres = ['fantasy', 'computer', 'history', 'bestsellers']


def gen_iterated_urls(base_url, genre, max_inc):
    urls = []

    for num in range(1, max_inc + 1):
        urls.append({'url': base_url + genre + '/page/' + str(num), 'genre': genre, 'page': num})

    return urls


# print(gen_iterated_urls(base_url, 'fantasy', 10))


def page_list_all_genres(base_url, genres, number_of_pages):
    "Generate all URLs to scrape based on provided genres and page max."

    out_list = []

    for genre in genres:
        genre_urls = gen_iterated_urls(base_url, genre, number_of_pages)
        out_list += genre_urls

    return out_list

# Delete old files before running scraper
for genre in genres:
    genre_filename = "%s.html" % genre

    if os.path.exists(genre_filename):
        os.remove(genre_filename)


class Audiobooks(scrapy.Spider):
    name = "audiobooks"

    def start_requests(self):


        pages = page_list_all_genres(base_url, genres, number_of_pages)


        for page in pages:
            yield scrapy.Request(meta=page, url=page['url'], callback=self.parse)

    def parse(self, response):

        relative_book_urls = response.css('h2').css('a').extract()

        absolute_book_urls = []

        for url in relative_book_urls:
            absolute_book_url  = url.replace('/audio-books/', single_book_url)

            absolute_book_urls.append(absolute_book_url)


            
        filename = '%s.html' % (response.meta['genre'])
        
        with open(filename, 'a') as f:
            for url in absolute_book_urls:
                f.write('<p>')
                f.write(url)
                f.write('</p>')
        self.log('Saved file %s' % filename)
        
