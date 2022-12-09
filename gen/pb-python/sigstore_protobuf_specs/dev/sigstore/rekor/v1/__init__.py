# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: sigstore_rekor.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import List

import betterproto

from ...common import v1 as __common_v1__


@dataclass(eq=False, repr=False)
class KindVersion(betterproto.Message):
    """KindVersion contains the entry's kind and api version."""

    kind: str = betterproto.string_field(1)
    """
    Kind is the type of entry being stored in the log. See here for a list:
    https://github.com/sigstore/rekor/tree/main/pkg/types
    """

    version: str = betterproto.string_field(2)
    """The specific api version of the type."""


@dataclass(eq=False, repr=False)
class Checkpoint(betterproto.Message):
    """
    The checkpoint contains a signature of the tree head (root hash), size of
    the tree, the transparency log's unique identifier (log ID), hostname and
    the current time. The result is a string, the format is described here
    https://github.com/transparency-dev/formats/blob/main/log/README.md The
    details are here https://github.com/sigstore/rekor/blob/a6e58f72b6b18cc06ce
    fe61808efd562b9726330/pkg/util/signed_note.go#L114 The signature has the
    same format as InclusionPromise.signed_entry_timestamp. See below for more
    details.
    """

    envelope: str = betterproto.string_field(1)


@dataclass(eq=False, repr=False)
class InclusionProof(betterproto.Message):
    """
    InclusionProof is the proof returned from the transparency log. Can be used
    for on line verification against the log.
    """

    log_index: int = betterproto.int64_field(1)
    """The index of the entry in the log."""

    root_hash: bytes = betterproto.bytes_field(2)
    """
    The hash digest stored at the root of the merkle tree at the time the proof
    was generated.
    """

    tree_size: int = betterproto.int64_field(3)
    """The size of the merkle tree at the time the proof was generated."""

    hashes: List[bytes] = betterproto.bytes_field(4)
    """
    A list of hashes required to compute the inclusion proof, sorted in order
    from leaf to root. Not that leaf and root hashes are not included. The root
    has is available separately in this message, and the leaf hash should be
    calculated by the client.
    """

    checkpoint: "Checkpoint" = betterproto.message_field(5)
    """
    Signature of the tree head, as of the time of this proof was generated. See
    above info on 'Checkpoint' for more details.
    """


@dataclass(eq=False, repr=False)
class InclusionPromise(betterproto.Message):
    """
    The inclusion promise is calculated by Rekor. It's calculated as a
    signature over a canonical JSON serialization of the persisted entry, the
    log ID, log index and the integration timestamp. See https://github.com/sig
    store/rekor/blob/a6e58f72b6b18cc06cefe61808efd562b9726330/pkg/api/entries.g
    o#L54 The format of the signature depends on the transparency log's public
    key. If the signature algorithm requires a hash function and/or a signature
    scheme (e.g. RSA) those has to be retrieved out-of-band from the log's
    operators, together with the public key. This is used to verify the
    integration timestamp's value and that the log has promised to include the
    entry.
    """

    signed_entry_timestamp: bytes = betterproto.bytes_field(1)


@dataclass(eq=False, repr=False)
class TransparencyLogEntry(betterproto.Message):
    """
    TransparencyLogEntry captures all the details required from Rekor to
    reconstruct an entry, given that the payload is provided via other means.
    This type can easily be created from the existing response from Rekor.
    Future iterations could rely on Rekor returning the minimal set of
    attributes (excluding the payload) that are required for verifying the
    inclusion promise. The inclusion promise (called SignedEntryTimestamp in
    the response from Rekor) is similar to a Signed Certificate Timestamp as
    described here https://www.rfc-editor.org/rfc/rfc9162#name-signed-
    certificate-timestam.
    """

    log_index: int = betterproto.int64_field(1)
    """The index of the entry in the log."""

    log_id: "__common_v1__.LogId" = betterproto.message_field(2)
    """The unique identifier of the log."""

    kind_version: "KindVersion" = betterproto.message_field(3)
    """
    The kind (type) and version of the object associated with this entry. These
    values are required to construct the entry during verification.
    """

    integrated_time: int = betterproto.int64_field(4)
    """The UNIX timestamp from the log when the entry was persisted."""

    inclusion_promise: "InclusionPromise" = betterproto.message_field(5)
    """The inclusion promise/signed entry timestamp from the log."""

    inclusion_proof: "InclusionProof" = betterproto.message_field(6)
    """
    The inclusion proof can be used for online verification that the entry was
    appended to the log, and that the log has not been altered.
    """

    canonicalized_body: bytes = betterproto.bytes_field(7)
    """
    The canonicalized Rekor entry body, used for SET verification. This is the
    same as the body returned by Rekor. It's included here for cases where the
    client cannot deterministically reconstruct the bundle from the other
    fields. Clients MUST verify that the signature referenced in the
    canonicalized_body matches the signature provided in the bundle content.
    """