
--Pivot

with vendas_unidade as (
	select 
	x.totalVenda
	,x.unidadeId 
	,x.unidadeId as loja
	,x.lojanome
	,x.uf
	,(SELECT COUNT(*) FROM BI.dbo.pedidos_valores as v
	where v.unidadeId = x.unidadeId
	group by v.unidadeId) tot
	from BI.dbo.fato_venda as x
	)
	select *
	from vendas_unidade
	 pivot
	 (
		SUM(totalVenda)
		FOR lojanome IN ("Pelotas","Indaiatuba")
	 )a
order by a.unidadeId	




--Consulta Log

with contagem as (
 SELECT DISTINCT
      stlog.relacionamentoId
     ,(
		SELECT COUNT(*)
	 from [189.39.29.24].[dbo].[RelacionamentoStatusLog] as slog
	 where slog.relacionamentoId = stlog.relacionamentoId
	 group by  slog.relacionamentoId
	 ) frequencia
  FROM [189.39.29.24].[dbo].[RelacionamentoStatusLog] as stlog
  left join [BI].[comercial].[dim_interacoes_leads] as leads on leads.ref_lead = stlog.relacionamentoId)


  UPDATE leads
  set leads.TOTALINTERACOES = ct.frequencia

  from [BI].[comercial].[dim_interacoes_leads] as leads
  left join contagem as ct on ct.relacionamentoId  = leads.ref_lead



--Trigger Consulta "Eu nao lembro o que ela fazia"

CREATE OR ALTER TRIGGER TG_carga_dimensao_lead
ON [comercial].[classificacao_leads]
AFTER INSERT, UPDATE, DELETE
AS
BEGIN

DECLARE
@ref_lead INT, @ref_loja INT, @datacadastrolog DATETIME,@idstatuslead INT

	WITH tabela_leads AS (

	select ref_lead, statusId, unidadeId,dataatualizado FROM
		comercial.classificacao_leads

	)

	select * from tabela_leads

	select a.ref_lead
	,a.dataUltimaInteracao
	,a.STATUSATUAL,a.statusId as idatual
	,a.campanha as atual
	,logv.statusId
	,logv.dataCadastro
	,(select count(*) from [189.39.29.24].[dbo].[RelacionamentoStatusLog] as b where a.ref_lead=b.relacionamentoId) total_iteracoeslog
	,(select top(1) b.dataCadastro from [189.39.29.24].[dbo].[RelacionamentoStatusLog]  b where a.ref_lead = b.relacionamentoId ) as statusidlog
	from [BI].[comercial].[classificacao_leads] as a
	left join [189.39.29.24].[dbo].[RelacionamentoStatusLog]  as logv on logv.relacionamentoId = a.ref_lead
	where a.ref_lead  in (select relacionamentoId from [189.39.29.24].[dbo].[RelacionamentoStatusLog] 
	where relacionamentoId = ref_lead) and ref_lead = a.ref_lead
	
	
--Trigger "Update"

CREATE OR ALTER TRIGGER TG_carga_status_log
ON [comercial].[classificacao_leads]
AFTER INSERT,DELETE 
AS
BEGIN
		
UPDATE leads
			SET [IteracoesStatusLog2] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog3] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog4] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog5] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog6] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog7] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog8] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog9] = (CASE WHEN  slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END),
				[IteracoesStatusLog10] = (CASE WHEN slog.relacionamentoId = leads.ref_lead THEN slog.statusId ELSE NULL END)
						
	
FROM [BI].[comercial].[classificacao_leads] as leads
left join [189.39.29.24].[dbo].[RelacionamentoStatusLog]  as slog on slog.relacionamentoId = leads.ref_lead

END	
	


	
--Consulta "CLiente Interacoes"
with contagem as (
 SELECT DISTINCT
      stlog.relacionamentoId
     ,(
		SELECT COUNT(*)
	 from [189.39.29.24].[dbo].[RelacionamentoStatusLog] as slog
	 where slog.relacionamentoId = stlog.relacionamentoId
	 group by  slog.relacionamentoId
	 ) frequencia
  FROM [189.39.29.24].[dbo].[RelacionamentoStatusLog] as stlog
  left join [BI].[comercial].[dim_interacoes_leads] as leads on leads.ref_lead = stlog.relacionamentoId)


  UPDATE leads
  set leads.TOTALINTERACOES = ct.frequencia

  from [BI].[comercial].[dim_interacoes_leads] as leads
  left join contagem as ct on ct.relacionamentoId  = leads.ref_lead
  
  
  
  
 /****** Market Basket ******/
WITH market_basket AS (

	select DISTINCT
		v.numeracao    
		,vitem.produtoId
		,p.nome
 
  FROM myboxmarcenaria.dbo.VendaItem AS vitem
	LEFT JOIN dbo.Venda as v on v.id = vitem.vendaId
	left join [dbo].[Produto] as p on p.id = vitem.produtoId
	
	)

SELECT distinct
	a.nome,
	b.nome,
	COUNT(*) AS frequencia

FROM market_basket  a
inner join market_basket b  on a.numeracao = b.numeracao and a.produtoId = b.produtoId

GROUP BY a.nome,b.nome
ORDER BY COUNT(*) DESC





