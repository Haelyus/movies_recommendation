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
    str_comment = "Type '/recommendation/id/' for movies recommendation by id \r"
    str_comment = str_comment + "or \r"
    str_comment = str_comment + "type '/recommendation/title/' for movies recommendation by title..."
    return str_comment
@app.route('/recommendation/id/')
def id():
    return "Enter an id movie..."
@app.route('/recommendation/id/<string:s_query>', methods = ['GET'])
def id_movie(s_query):
    s_query_movie, d_query, d_recommendation = movie_recommendation.recommendation(id_title = s_query, index = True)
    if s_query_movie != "":
        return jsonify(d_query, d_recommendation)
    else:
        str_recommend = 'The movie with "'+ s_query +'" id is unknown.'
        return str_recommend
@app.route('/recommendation/title/')
def title():
    return "Enter a title movie..."
@app.route('/recommendation/title/<string:s_query>', methods = ['GET'])
def title_movie(s_query):
    s_query_movie, d_query, d_recommendation = movie_recommendation.recommendation(id_title = s_query)
    if s_query_movie != "":
        return jsonify(d_query, d_recommendation)
    else:
        str_recommend = 'The "'+ s_query +'" movie is unknown.'
        return str_recommend
   
        
if __name__ == "__main__":
#lance le serveur Flask
    #Lance app sur le port 8080 en mode debug
    app.run(host="0.0.0.0",debug=True, port = 8080)
