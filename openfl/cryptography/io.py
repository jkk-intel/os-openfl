# Copyright 2020-2024 Intel Corporation
# SPDX-License-Identifier: Apache-2.0


"""Cryptography IO utilities."""

import os
from hashlib import sha384
from pathlib import Path
from typing import Tuple

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.x509.base import Certificate, CertificateSigningRequest


def read_key(path: Path) -> RSAPrivateKey:
    """
    Read private key.

    Args:
        path : Path (pathlib)

    Returns:
        private_key
    """
    with open(path, "rb") as f:
        pem_data = f.read()

    signing_key = load_pem_private_key(pem_data, password=None)
    # TODO: replace assert with exception / sys.exit
    assert isinstance(signing_key, rsa.RSAPrivateKey)
    return signing_key


def write_key(key: RSAPrivateKey, path: Path) -> None:
    """
    Write private key.

    Args:
        key  : RSA private key object
        path : Path (pathlib)

    """

    def key_opener(path, flags):
        return os.open(path, flags, mode=0o600)

    with open(path, "wb", opener=key_opener) as f:
        f.write(
            key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def read_crt(path: Path) -> Certificate:
    """
    Read signed TLS certificate.

    Args:
        path : Path (pathlib)

    Returns:
        Cryptography TLS Certificate object
    """
    with open(path, "rb") as f:
        pem_data = f.read()

    certificate = x509.load_pem_x509_certificate(pem_data)
    # TODO: replace assert with exception / sys.exit
    assert isinstance(certificate, x509.Certificate)
    return certificate


def write_crt(certificate: Certificate, path: Path) -> None:
    """
    Write cryptography certificate / csr.

    Args:
        certificate : cryptography csr / certificate object
        path : Path (pathlib)

    Returns:
        Cryptography TLS Certificate object
    """
    with open(path, "wb") as f:
        f.write(
            certificate.public_bytes(
                encoding=serialization.Encoding.PEM,
            )
        )


def read_csr(path: Path) -> Tuple[CertificateSigningRequest, str]:
    """
    Read certificate signing request.

    Args:
        path : Path (pathlib)

    Returns:
        Cryptography CSR object
    """
    with open(path, "rb") as f:
        pem_data = f.read()

    csr = x509.load_pem_x509_csr(pem_data)
    # TODO: replace assert with exception / sys.exit
    assert isinstance(csr, x509.CertificateSigningRequest)
    return csr, get_csr_hash(csr)


def get_csr_hash(certificate: CertificateSigningRequest) -> str:
    """
    Get hash of cryptography certificate.

    Args:
        certificate : Cryptography CSR object

    Returns:
        Hash of cryptography certificate / csr
    """
    hasher = sha384()
    encoded_bytes = certificate.public_bytes(
        encoding=serialization.Encoding.PEM,
    )
    hasher.update(encoded_bytes)
    return hasher.hexdigest()
