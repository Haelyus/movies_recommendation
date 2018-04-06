from flask import Flask, jsonify
import movie_recommendation

#déclare le serveur flask
app = Flask(__name__)

#crée la route web de la racine du site 
#et la lie à la fonction welcome
@app.route("/")
def welcome():
    return "Welcome to the Movies Recommendation !"

@app.route('/recommendation/')
def type_movie():
    return "Enter a movie title..."
@app.route('/recommendation/<string:title>', methods = ['GET'])
def query_movie(title):
    s_query_movie, l_recommendation = movie_recommendation.recommendation(movie_title = title)
    if s_query_movie != "":
        str_recommend = 'Recommendations for "' + str(s_query_movie) + '" '
        return jsonify({str_recommend : str(l_recommendation) })
    else:
        str_recommend = 'The "'+ title +'" movie is unknown.'
        return str_recommend
   
        
if __name__ == "__main__":
#lance le serveur Flask
    #Lance app sur le port 8080 en mode debug
    app.run(host="0.0.0.0",debug=True, port = 8080)
