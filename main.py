from flask import Flask, Blueprint, render_template, request

app = Flask(__name__)

# Blueprint for Prim's algorithm
prim_bp = Blueprint('prim', __name__)

def primsAlgorithm(vertices, edges):
    adjacencyMatrix = [[0 for _ in range(vertices)] for _ in range(vertices)]
    mstMatrix = [[0 for _ in range(vertices)] for _ in range(vertices)]

    for edge in edges:
        i, j, weight = edge
        adjacencyMatrix[i][j] = weight
        adjacencyMatrix[j][i] = weight

    positiveInf = float('inf')
    selectedVertices = [False] * vertices

    while False in selectedVertices:
        minimum = positiveInf
        start, end = 0, 0

        for i in range(vertices):
            if selectedVertices[i]:
                for j in range(i, vertices):
                    if not selectedVertices[j] and adjacencyMatrix[i][j] > 0:
                        if adjacencyMatrix[i][j] < minimum:
                            minimum = adjacencyMatrix[i][j]
                            start, end = i, j

        selectedVertices[end] = True
        mstMatrix[start][end] = minimum
        mstMatrix[end][start] = mstMatrix[start][end]

    return mstMatrix

@prim_bp.route('/prim', methods=['GET', 'POST'])
def prim():
    if request.method == 'POST':
        try:
            vertices = int(request.form['vertices'])
            edges_input = request.form['edges']
            edges_list = [tuple(map(int, edge.split())) for edge in edges_input.split(', ')]

            mst_matrix = primsAlgorithm(vertices, edges_list)

            return render_template('index.html', mst_matrix=mst_matrix, vertices=vertices)
        except (ValueError, IndexError):
            return render_template('index.html', mst_matrix=None, vertices=None, error_message="Invalid input format")

    return render_template('index.html', mst_matrix=None, vertices=None)

app.register_blueprint(prim_bp)

# Rest of your code...

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
