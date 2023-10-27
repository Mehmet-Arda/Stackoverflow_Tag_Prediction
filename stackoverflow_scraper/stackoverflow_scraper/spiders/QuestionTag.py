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

        #"DOWNLOAD_DELAY" : 2.5, #Default 0,
        "AUTOTHROTTLE_START_DELAY" : 8, #Default 5
        "RANDOMIZED _DOWNLOAD_DELAY" : True, #Default False
        "COOKIES_ENABLED" : False, #Default True
        "AUTOTHROTTLE_ENABLED" : True, #Default False
        "AUTOTHROTTLE_TARGET_CONCURRENCY" : 1, #Default 1
        "AUTOTHROTTLE_DEBUG" : True,
        "CONCURRENT_REQUESTS" : 11, #Default 16
        "ROBOTSTXT_OBEY" : True #Default False
    }


    # allowed_domains = ["stackoverflow.com"]
    # start_urls = ["https://stackoverflow.com/questions"]


    def start_requests(self):

        self.base_url = "https://stackoverflow.com"

        self.tags_page_url = "/tags?page={page_number}&tab=popular"

        self.question_summaries_url = "/questions/tagged/{tag_name}?tab=votes&page={page_number}"

        self.question_detail_page_url_suffix = "?answertab=createdasc"
        self.tags_page_number = 1

        
        self.number_of_questions_per_tag = 100
        
        
        self.tags_page_final_url = self.base_url + self.tags_page_url.format(page_number = self.tags_page_number)

        yield scrapy.Request(url = self.tags_page_final_url , callback = self.parse_tags_page)



    def parse_tags_page(self, response):

        tag_question_link_list = response.css("#tags_list .js-tag-cell a.post-tag")
        tag_question_count_list = response.css("#tags_list .js-tag-cell div:nth-child(3) div:first-child::text").getall()

        tag_question_count_list = map(lambda x : int(x.split()[0]), tag_question_count_list)

        for x in range(36):
            if tag_question_count_list[x] >= 3000:

                tag_name = tag_question_link_list[x].attrib["href"].split("/")[3]
                
                question_summaries_page_final_url = self.base_url + self.question_summaries_url.format(tag_name = tag_name , page_number = 1,) 

                scrapy.Request(url = question_summaries_page_final_url, callback = self.parse_question_summaries_page)

        for y in range(1):
            self.tags_page_number += 1
            scrapy.Request(url = self.tags_page_final_url.format(p = self.tags_page_number), callback = self.parse_tags_page)
        #.css("#tags_list .js-tag-cell a.post-tag")[2].attrib["href"] /questions/tagged/javascript'
        #.css("#tags_list .js-tag-cell div:nth-child(3) div:first-child::text").get() '2516889 questions'
        

        

    
    def parse_question_summaries_page(self, response):
        
        question_summaries = response.css("#questions .s-post-summary")

        tag_name = response.url.split("{")[1].split("}")[0]
        page_number = int(response.url.split("{")[2].strip("}"))

        # global total_page_count

        # if page_number == 1:
            
        #     total_page_count = response.css(".s-pagination.pager a:nth-child(7)::text").get()
        

        for i in range(50):

            question_detail_page_url = question_summaries[i].css(".s-post-summary--content-title .s-link").attrib["href"]

            if len(question_summaries[i].css(".s-post-summary--meta .s-user-card time.s-user-card--time:empty")) == 0: # []
                    
                    question_detail_page_final_url = self.base_url + question_detail_page_url + self.question_detail_page_url_suffix
                    yield scrapy.Request(url = question_detail_page_final_url , callback = self.parse_question_detail_page)

            
        page_number += 1

        question_summaries_page_final_url = self.base_url + self.question_summaries_url.format(tag_name = tag_name , page_number = page_number) 

        if page_number <= self.number_of_questions_per_tag / 50:

            yield scrapy.Request(url =  question_summaries_page_final_url ,callback = self.parse_question_summaries_page)
            
        


    def parse_question_detail_page(self, response):

        stackoverflow_qt_item = StackoverflowQTItems()

        question_detail_page = response

        stackoverflow_qt_item["title"] = question_detail_page.css("#question-header .question-hyperlink::text").get()
        stackoverflow_qt_item["content"] = question_detail_page.css(".question .postcell .s-prose.js-post-body").getall()
        stackoverflow_qt_item["score"] = question_detail_page.css(".question .votecell .js-vote-count::text").get()
        stackoverflow_qt_item["views"] = question_detail_page.css("#question-header + div div[title ^= Viewed]").attrib["title"]
        stackoverflow_qt_item["tags"] = question_detail_page.css(".question .postcell .post-taglist li a.post-tag::text").getall()
        stackoverflow_qt_item["creation_date"] = question_detail_page.css("#question-header + div time[itemprop='dateCreated']").attrib["datetime"]
        stackoverflow_qt_item["answer_count"] = question_detail_page.css("#answers #answers-header h2[data-answercount]").attrib["data-answercount"]
        stackoverflow_qt_item["first_answer_date"] = question_detail_page.css("#answers .answer[data-position-on-page = '1'] .answercell time[itemprop = 'dateCreated']").attrib["datetime"]        

        yield stackoverflow_qt_item