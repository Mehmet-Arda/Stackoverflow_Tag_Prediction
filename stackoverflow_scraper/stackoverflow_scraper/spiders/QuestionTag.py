from typing import Iterable
import scrapy
from scrapy.http import Request
from stackoverflow_scraper.items import StackoverflowQTItems
from datetime import datetime

class QuestiontagSpider(scrapy.Spider):
    name = "QuestionTag"

    custom_settings = {
        "FEEDS" : {
            "stackoverflow_data.json" : { "format" : "json", "encoding" : "utf-8", "overwrite" : True}
        },

        "DOWNLOAD_DELAY" : 2.5, #Default 0,
        "AUTOTHROTTLE_START_DELAY" : 8, #Default 5
        "RANDOMIZED _DOWNLOAD_DELAY" : True, #Default False
        "COOKIES_ENABLED" : False, #Default True
        "AUTOTHROTTLE_ENABLED" : True, #Default False
        "AUTOTHROTTLE_TARGET_CONCURRENCY" : 0.5, #Default 1
        #"CONCURRENT_REQUESTS" : 8, #Default 16
        "ROBOTSTXT_OBEY" : True #Default False
    }


    # allowed_domains = ["stackoverflow.com"]
    # start_urls = ["https://stackoverflow.com/questions"]

    # number_of_questions_per_year = {
    #     "2008" : 0,
    #     "2009" : 0,
    #     "2010" : 0,
    #     "2011" : 0,
    #     "2012" : 0,
    #     "2013" : 0,
    #     "2014" : 0,
    #     "2015" : 0,
    #     "2016" : 0,
    #     "2017" : 0,
    #     "2018" : 0,
    #     "2019" : 0,
    #     "2020" : 0,
    #     "2021" : 0,
    #     "2022" : 0,
    #     "2023" : 0
    # }


    def start_requests(self):

        self.base_url = "https://stackoverflow.com"

        self.question_detail_page_url_suffix = "?answertab=createdasc"

        self.question_summaries_url = "https://stackoverflow.com/questions?tab=votes&page={p}"

        self.page = 1

        self.question_count = 100
        self.number_of_questions_per_year = {}
        year = 2008

        for i in range((datetime.now().year - 2008) + 1 ):
            
            self.number_of_questions_per_year[str(year)] = 0
            year += 1
        
        yield scrapy.Request(self.question_summaries_url.format(p = self.page))

    def parse(self, response):

        question_summaries = response.css("#questions .s-post-summary")

        if self.page == 1:
            self.total_page_count = response.css(".s-pagination.pager a:nth-child(7)::text").get()

        
        
        

        

        for i in range(50):

            print("++++++++++++++++++++++")
            print(i)

            question_detail_page_url = question_summaries[i].css(".s-post-summary--content-title .s-link").attrib["href"]

            if len(question_summaries[i].css(".s-post-summary--meta .s-user-card time.s-user-card--time:empty")) == 0: # []
                
                print("-+-+-+-+-++-+-+")
                print(i)
                question_created_date = question_summaries[i].css(".s-post-summary--meta .s-user-card time.s-user-card--time span").attrib["title"]

                question_created_date = datetime.fromisoformat(question_created_date)

                if self.number_of_questions_per_year[str(question_created_date.year)] < self.question_count:
                    
                    yield scrapy.Request(url = self.base_url + question_detail_page_url + self.question_detail_page_url_suffix , callback = self.parse_question_detail_page , cb_kwargs={"isCommunityWiki" : False})

                
            else:
                
                yield scrapy.Request(url = self.base_url + question_detail_page_url + self.question_detail_page_url_suffix , callback = self.parse_question_detail_page , cb_kwargs={"isCommunityWiki" : True})


            

            


        print("------------------------------")
        print(list(self.number_of_questions_per_year.values()).count(self.question_count))
        print("------------------------------")
        print(list(self.number_of_questions_per_year.values()))
        print("------------------------------")
        print(len(self.number_of_questions_per_year))

        if list(self.number_of_questions_per_year.values()).count(self.question_count) != len(self.number_of_questions_per_year):
            
            self.page += 1

            print("******************")
            print(self.page)
            print(self.total_page_count)

            #self.page <= int(self.total_page_count)
            if self.page <= 3:

                yield scrapy.Request(url =  self.question_summaries_url.format(p = self.page) ,callback=self.parse)
            

        
        
    def parse_question_detail_page(self, response , isCommunityWiki):

        stackoverflow_qt_item = StackoverflowQTItems()

        question_detail_page = response

        print("*****************************************************")
        print(self.number_of_questions_per_year.items())
        print(self.page)

        stackoverflow_qt_item["title"] = question_detail_page.css("#question-header .question-hyperlink::text").get()
        stackoverflow_qt_item["content"] = question_detail_page.css(".question .postcell .s-prose.js-post-body").getall()
        stackoverflow_qt_item["score"] = question_detail_page.css(".question .votecell .js-vote-count::text").get()
        stackoverflow_qt_item["views"] = question_detail_page.css("#question-header + div div[title ^= Viewed]").attrib["title"]
        stackoverflow_qt_item["tags"] = question_detail_page.css(".question .postcell .post-taglist li a.post-tag::text").getall()
        stackoverflow_qt_item["creation_date"] = question_detail_page.css("#question-header + div time[itemprop='dateCreated']").attrib["datetime"]
        stackoverflow_qt_item["answer_count"] = question_detail_page.css("#answers #answers-header h2[data-answercount]").attrib["data-answercount"]
        stackoverflow_qt_item["first_answer_date"] = question_detail_page.css("#answers .answer[data-position-on-page = '1'] .answercell time[itemprop = 'dateCreated']").attrib["datetime"]
        
        

        if isCommunityWiki:

            question_created_date = datetime.fromisoformat(stackoverflow_qt_item["creation_date"])

            if self.number_of_questions_per_year[str(question_created_date.year)] < self.question_count:

                self.number_of_questions_per_year[str(question_created_date.year)] += 1

                yield stackoverflow_qt_item

        else:
            yield stackoverflow_qt_item