from database.DB_connect import DBConnect
from modell.state import State


class DAO:
    @staticmethod
    def get_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  year(s.s_datetime) as year
                    FROM  sighting s
                    WHERE year(s.s_datetime) >= 1910 AND year(s.s_datetime) <= 2014
                    GROUP BY year(s.s_datetime)"""

        cursor.execute(query)

        for row in cursor:
            result.append(int(row['year']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_shape(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT  s.shape
                        FROM  sighting s
                        WHERE YEAR(s.s_datetime) = %s
                        GROUP BY s.shape"""

        cursor.execute(query, (anno,))
        counter = 0

        for row in cursor:
            if counter == 0:
                counter += 1
            else:
                result.append(row['shape'])
                counter += 1


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_state():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  id, name, lat, lng
                   FROM state
                   GROUP by id"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(row['id'], row['name'], row['lat'], row['lng']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_connessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  state1, state2
                   FROM neighbor
                   WHERE state1 < state2"""

        cursor.execute(query)

        for row in cursor:
            result.append((row['state1'], row['state2']))

        cursor.close()
        conn.close()
        return result



    @staticmethod
    def get_peso(anno, forma):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """SELECT state, COUNT(s_datetime) AS peso
                   FROM sighting
                   WHERE YEAR(s_datetime) = %s
                   AND shape = %s
                   GROUP BY state"""

        cursor.execute(query, (anno,forma,))

        for row in cursor:
            result[str(row['state']).upper()] = int(row['peso'])

        cursor.close()
        conn.close()
        return result