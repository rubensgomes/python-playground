"""rgapps.http.resources.units.temperature module

This module contains the REST API source code for temperature conversions.
"""
from collections import OrderedDict

from flask import request, jsonify
from flask_restful import Resource
from werkzeug.exceptions import BadRequest

from rgapps.constants import STATUS_KEY, STATUS_SUCCESS, DATA_KEY
from rgapps.domain.units.temperature import Temperature
from rgapps.utils.utility import is_number


__author__ = "Rubens S. Gomes <rubens.s.gomes@gmail.com>"
__copyright__ = "Copyright (c) 2015 Rubens S. Gomes"
__license__ = "All Rights Reserved"
__maintainer__ = "Rubens Gomes"
__email__ = "rubens.s.gomes@gmail.com"
__status__ = "Experimental"

__all__ = ["RESTTemperatureResource"]


class RESTTemperatureResource( Resource ):
    """REST API Resource to convert temperatures
    """

    def get( self, to_unit ):
        """REST GET implementation for the URI:

        http://<server>:<port>/temperature/<to_unit>?from_unit=<from_unit>&
            from_value=<from_value>

        Parameters
        ----------
        to_unit:  str (required)
            Temperature unit (required)

        It is assumed that this method is called within the context of an HTTP
        request.  And that the HTTP request contains query parameters
        with the request.args as containing the following:

        from_unit: str (required)
            length unit
        from_value: str (required)
            numeric value

        Returns
        -------
        str:
            A JSON string containing the response

        Raises
        ------
        BadRequest if there is an error validating the input parameters or
        some other error processing this method.
        """
        params = request.args
        if not params:
            raise BadRequest( "Parameters "
                             "from_unit=<from_unit>&from_value=<_from_value> "
                             "are missing" )

        if not isinstance( params, dict ):
            raise BadRequest( "params must be an instance of dict" )

        if "from_unit" not in params:
            raise BadRequest( "Missing required from_unit parameter" )

        if "from_value" not in params:
            raise BadRequest( "Missing required from_value parameter" )

        from_unit = params.get( "from_unit" )

        from_value = params.get( "from_value" )
        if not is_number( from_value ):
            raise BadRequest( ( "Parameter from_value=[{0}] not valid. "
                              "A numeric value must be provided." )
                             .format( from_value ) )

        from_value = float( from_value )

        if from_unit == to_unit:
            raise BadRequest( "from_unit=[{0}] and to_unit=[{1}] units "
                             "cannot be equal".format( from_unit, to_unit ) )

        # pint temperature units need to be lower-cased or degC, degF, degK
        from_unit = from_unit.lower().strip()
        if from_unit == "degc":
            from_unit = "degC"
        elif from_unit == "degf":
            from_unit = "degF"
        elif from_unit == "degk":
            from_unit = "degK"

        # pint temperature units need to be lower-cased or degC, degF, degK
        to_unit = to_unit.lower().strip()
        if to_unit == "degc":
            to_unit = "degC"
        elif to_unit == "degf":
            to_unit = "degF"
        elif to_unit == "degk":
            to_unit = "degK"

        result = Temperature.convert( from_value, from_unit, to_unit )

        data = OrderedDict()
        data["from_unit"] = from_unit
        data["from_value"] = from_value
        data["to_unit"] = to_unit
        data["to_value"] = result

        response = OrderedDict()
        response[STATUS_KEY] = STATUS_SUCCESS
        response[DATA_KEY] = data

        json_result = jsonify( response )
        return json_result


if __name__ == "__main__":
    pass
