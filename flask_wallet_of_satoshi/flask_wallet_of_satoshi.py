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
        self._wallet = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Initializes the Flask application object.

        Args:
            app: Flask application object.
        """
        self.app = app
        self._set_wallet()
        app.route("/.well-known/lnurlp/pay")(self.well_known)
        app.route(f"/lightning/lnurl/pay/{self.username_alias}")(self.pay_request)

    def _set_wallet(self):
        """
        Sets up the Wallet of Satoshi instance.

        Returns:
            A JSON response with the error message and status code 500 if the username is not configured.
        """
        username = self.app.config.get("WOS_USERNAME")
        username_alias = self.app.config.get("WOS_USERNAME_ALIAS")
        if not username:
            return jsonify({"error": "Wallet of Satoshi username not configured."}), 500

        self._wallet = _WalletOfSatoshi(username)

    def well_known(self):
        """
        Handles the lnurlp/pay/<username_alias> route.

        Returns:
            A JSON response with the lnurlp data.
        """
        if not self._wallet:
            return jsonify({"error": "Wallet not initialized."}), 500

        data = self._wallet.well_known()
        return jsonify(data)

    def pay_request(self):
        """
        Handles the lightning/lnurl/pay route.

        Returns:
            The payment request.
        """
        if not self._wallet:
            return jsonify({"error": "Wallet not initialized."}), 500

        amount = request.args.get("amount")
        if not amount:
            return (
                jsonify(
                    {"error": "Integer amount parameter in millisatoshis is missing."}
                ),
                400,
            )

        data = self._wallet.pay_request(amount=amount)
        return data
