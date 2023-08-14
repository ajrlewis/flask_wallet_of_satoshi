from flask import jsonify, request
from wallet_of_satoshi import WalletOfSatoshi as _WalletOfSatoshi


class WalletOfSatoshi:
    """
    Wrapper class for interacting with Wallet of Satoshi API.
    """

    def __init__(self, app=None):
        """
        Initializes the WalletOfSatoshi object.

        Args:
            app: Flask application object (optional).
        """
        self.app = app
        self.wallet = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Flask application object.

        Args:
            app: Flask application object.
        """
        self.app = app
        app.route("/.well-known/lnurlp/pay")(self.lnurl_pay)
        app.route("/lightning/payment-request")(self.payment_request)

        @app.errorhandler(500)
        def handle_error(error):
            """
            Error handler for 500 Internal Server Error.

            Args:
                error: The error object.

            Returns:
                A JSON response with the error message and status code 500.
            """
            return jsonify({"error": "Wallet of Satoshi username not configured."}), 500

        self.set_wallet()

    def set_wallet(self):
        """
        Sets up the Wallet of Satoshi instance.

        Returns:
            A JSON response with the error message and status code 500 if the username is not configured.
        """
        username = self.app.config.get("WOS_USERNAME")
        if not username:
            return jsonify({"error": "Wallet of Satoshi username not configured."}), 500

        display_name = self.app.config.get("WOS_METADATA_PLAIN")
        self.wallet = _WalletOfSatoshi(username, display_name)

    def lnurl_pay(self):
        """
        Handles the lnurlp/pay route.

        Returns:
            A JSON response with the lnurlp data.
        """
        if not self.wallet:
            return jsonify({"error": "Wallet not initialized."}), 500

        lnurlp = self.wallet.well_known()
        return jsonify(lnurlp)

    def payment_request(self):
        """
        Handles the lightning/payment-request route.

        Returns:
            The payment request.
        """
        if not self.wallet:
            return jsonify({"error": "Wallet not initialized."}), 500

        amount = request.args.get("amount")
        if not amount:
            return jsonify({"error": "Amount parameter in mSatoshis is missing."}), 400

        pr = self.wallet.payment_request(amount=amount)
        return pr
