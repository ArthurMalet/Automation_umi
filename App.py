from flask import Flask, request, jsonify
import camelot
import base64
import tempfile

app = Flask(__name__)

@app.route('/parse-planning', methods=['POST'])
def parse_pdf():
    data = request.get_json()
    pdf_base64 = data['file']
    user_name = data.get('name', 'MALET')

    # Décode et écrit le fichier temporairement
    pdf_bytes = base64.b64decode(pdf_base64)
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp:
        temp.write(pdf_bytes)
        temp.flush()

        # Extraction de table
        try:
            tables = camelot.read_pdf(temp.name, pages="1", flavor='stream')
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        if not tables or len(tables) == 0:
            return jsonify([])

        result = []
        df = tables[0].df

        for i, row in df.iterrows():
            if row.isnull().any(): continue
            for j, cell in enumerate(row):
                if user_name.lower() in cell.lower():
                    periode = 'jour' if j == 1 else 'nuit'  # à adapter selon ton tableau
                    result.append({ "date": row[0], "periode": periode })
                    break

        return jsonify(result)
