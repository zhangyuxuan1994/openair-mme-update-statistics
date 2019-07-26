/*
 * Generated by asn1c-0.9.29 (http://lionet.info/asn1c)
 * From ASN.1 module "S1AP-CommonDataTypes"
 * 	found in "/home/lionel/EURECOM/CODE/openair-cn.prose.clean/src/s1ap/messages/asn1/r15/s1ap-15.1.0.asn1"
 * 	`asn1c -pdu=all -fcompound-names -fno-include-deps -gen-PER -no-gen-OER -no-gen-example -D /home/lionel/EURECOM/CODE/openair-cn.prose.clean/src/s1ap/messages/asn1/r15/GENERATED_S1AP`
 */

#include "S1AP_ProcedureCode.h"

int
S1AP_ProcedureCode_constraint(const asn_TYPE_descriptor_t *td, const void *sptr,
			asn_app_constraint_failed_f *ctfailcb, void *app_key) {
	long value;
	
	if(!sptr) {
		ASN__CTFAIL(app_key, td, sptr,
			"%s: value not given (%s:%d)",
			td->name, __FILE__, __LINE__);
		return -1;
	}
	
	value = *(const long *)sptr;
	
	if((value >= 0 && value <= 255)) {
		/* Constraint check succeeded */
		return 0;
	} else {
		ASN__CTFAIL(app_key, td, sptr,
			"%s: constraint failed (%s:%d)",
			td->name, __FILE__, __LINE__);
		return -1;
	}
}

/*
 * This type is implemented using NativeInteger,
 * so here we adjust the DEF accordingly.
 */
asn_per_constraints_t asn_PER_type_S1AP_ProcedureCode_constr_1 CC_NOTUSED = {
	{ APC_CONSTRAINED,	 8,  8,  0,  255 }	/* (0..255) */,
	{ APC_UNCONSTRAINED,	-1, -1,  0,  0 },
	0, 0	/* No PER value map */
};
static const ber_tlv_tag_t asn_DEF_S1AP_ProcedureCode_tags_1[] = {
	(ASN_TAG_CLASS_UNIVERSAL | (2 << 2))
};
asn_TYPE_descriptor_t asn_DEF_S1AP_ProcedureCode = {
	"ProcedureCode",
	"ProcedureCode",
	&asn_OP_NativeInteger,
	asn_DEF_S1AP_ProcedureCode_tags_1,
	sizeof(asn_DEF_S1AP_ProcedureCode_tags_1)
		/sizeof(asn_DEF_S1AP_ProcedureCode_tags_1[0]), /* 1 */
	asn_DEF_S1AP_ProcedureCode_tags_1,	/* Same as above */
	sizeof(asn_DEF_S1AP_ProcedureCode_tags_1)
		/sizeof(asn_DEF_S1AP_ProcedureCode_tags_1[0]), /* 1 */
	{ 0, &asn_PER_type_S1AP_ProcedureCode_constr_1, S1AP_ProcedureCode_constraint },
	0, 0,	/* No members */
	0	/* No specifics */
};
