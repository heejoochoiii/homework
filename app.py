from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_KEY = '9777155c8a3cc183254aee7ad5ebbafe'

# 한글 → 영어 매핑
city_map = {
    '서울': 'Seoul',
    '부산': 'Busan',
    '대구': 'Daegu',
    '인천': 'Incheon',
    '광주': 'Gwangju',
    '대전': 'Daejeon',
    '울산': 'Ulsan',
    '세종': 'Sejong',
    '수원': 'Suwon',
    '춘천': 'Chuncheon',
    '청주': 'Cheongju',
    '전주': 'Jeonju',
    '목포': 'Mokpo',
    '창원': 'Changwon',
    '진주': 'Jinju',
    '안동': 'Andong',
    '포항': 'Pohang',
    '강릉': 'Gangneung',
    '속초': 'Sokcho',
    '평택': 'Pyeongtaek',
    '김해': 'Gimhae',
    '양산': 'Yangsan',
    '구미': 'Gumi',
    '여수': 'Yeosu',
    '순천': 'Suncheon',
    '군산': 'Gunsan',
    '김천': 'Gimcheon',
    '제주': 'Jeju'
}


# 자동완성용 전체 리스트 (한글 + 영어)
autocomplete_list = list(city_map.keys()) + list(city_map.values())

@app.route('/')
def home():
    city_input = request.args.get('city', default='Seoul')

    # 한글이면 변환, 영어면 그대로 사용
    if city_input in city_map:
        city = city_map[city_input]
    else:
        city = city_input  # 사용자가 쓴 영어 그대로 (Busan, busan 등)

    weather = get_weather(city)

    return render_template('index.html', weather=weather)

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('q', '')
    # 대소문자 구분 없이 추천
    suggestions = [c for c in autocomplete_list if query.lower() in c.lower()]
    return jsonify(suggestions)

@app.route('/weather-data')
def weather_data():
    city = request.args.get('city', default='Seoul')
    weather = get_weather(city)
    return jsonify(weather)

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=kr'
    response = requests.get(url)
    data = response.json()

    if data.get('cod') != 200:
        return {
            'city': city,
            'error': f"'{city}'의 날씨를 찾을 수 없습니다. (영문 도시명은 첫 글자를 대문자로 입력하세요. 예: Busan)"
        }
    else:
        return {
            'city': city,
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'rain': data.get('rain', {}).get('1h', 0),
            'error': None
        }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
