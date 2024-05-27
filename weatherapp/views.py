from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse



def get_content(city):
        USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        LANGUAGE = "en-US,en;q=0.5"
        session = requests.Session()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE
        city=city.replace(' ','+')
        html_content = session.get(f'https://search.brave.com/search?q=weather+in+{city}').text
        return html_content


def mainpage(request):
    context = {}
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_content = get_content(city)
        soup = BeautifulSoup(html_content,'html.parser')
        city_name = soup.find('div',attrs={'id':'city-name'})
        if city_name:
            city_name = city_name.text
        else:
            return HttpResponse('Information not found. Unable to retrieve weather data.')
        date_element = soup.find('div',attrs={'id':'date'})
        if date_element:
            date_time = date_element.text
        image_weather = soup.find_all('div',attrs={'id':'weather-icon'})
        if image_weather:
            image_url = image_weather[0].find('img')['src'] if image_weather[0].find('img') else None
        degree = soup.find('div',attrs={'id':'weather-temp'}).text
        daily_buttons_div = soup.find('div', class_='daily-buttons noscrollbar svelte-5lvwe8')
        if daily_buttons_div:
            full_html_content = daily_buttons_div.prettify()
        context ={
            'city_name':city_name,
            'date_time':date_time,
            "image_url":image_url,
            'degree':degree,
            'full_html_content':full_html_content
        }
        
    return render(request,'index.html',context=context)
