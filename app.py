from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify
import resolvers as r

app = Flask(__name__)

type_defs = load_schema_from_path('schema.graphql')


mutation_query_graphql = MutationType()
mutation_query_graphql.set_field('add_student', r.resolve_student_create)
mutation_query_graphql.set_field('add_class', r.resolve_class_create)
mutation_query_graphql.set_field('add_student_to_class', r.resolve_add_student_to_class)


query_graphql = QueryType()
student_type = ObjectType('Student')
class_type = ObjectType('Class')

query_graphql.set_field('student_by_id', r.resolve_student_by_id)
query_graphql.set_field('class_by_id', r.resolve_class_by_id)
query_graphql.set_field('students', r.resolve_students)
query_graphql.set_field('classes', r.resolve_classes)
class_type.set_field('students', r.resolve_students_in_classes)

schema = make_executable_schema(type_defs, [student_type, class_type, query_graphql, mutation_query_graphql])


@app.route('/graphql', methods=['GET'])
def playground():
    return PLAYGROUND_HTML, 200


@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=None,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

